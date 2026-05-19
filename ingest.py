"""
One-shot loader for the knowledge base.

Reads the book, quotes, gifs, and HR docs, embeds them with Azure OpenAI,
and writes them into the Cosmos vector container.

Run ONCE after creating the Cosmos container. If you re-run it you'll end up
with duplicate rows (we mint a fresh UUID per item). Wipe the container first
if you need to reload.
"""

import os
import uuid
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.cosmos import CosmosClient, PartitionKey
from langchain_text_splitters import RecursiveCharacterTextSplitter

from data.quotes import arnold_quotes
from data.gifs import arnold_gifs
from data.hr_docs import documents

load_dotenv()

EMBED_MODEL = "text-embedding-ada-002"
BOOK_PATH = "data/book_txt.dm"

# Chunk settings, 2000/500 is a balance: large enough that multi-paragraph
# exercise descriptions stay together, with enough overlap that a query
# landing on the boundary still hits the right chunk.
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 500


# --- clients ---
oai = AzureOpenAI(
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
)

cosmos = CosmosClient(os.getenv("COSMOS_ENDPOINT"), os.getenv("COSMOS_KEY"))
db = cosmos.create_database_if_not_exists(id="AI_Database")
container = db.create_container_if_not_exists(
    id="EmbeddingsContainer",
    partition_key=PartitionKey(path="/id"),
)
print("Connected to Cosmos.")


def embed(text):
    return oai.embeddings.create(input=text, model=EMBED_MODEL).data[0].embedding


def push(text, searchable=None):
    # `searchable` lets us embed something different from what we store,
    # used for gifs where we want to match on tags but store the URL.
    container.upsert_item({
        "id": str(uuid.uuid4()),
        "text": text,
        "embedding": embed(searchable if searchable else text),
    })


# 1. Book
print(f"Reading book from {BOOK_PATH}...")
with open(BOOK_PATH, "r", encoding="utf-8") as f:
    book = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    is_separator_regex=False,
)
chunks = splitter.create_documents([book])
print(f"Book split into {len(chunks)} chunks. Pushing...")

for i, chunk in enumerate(chunks):
    push(chunk.page_content)
    if i and i % 20 == 0:
        print(f"  {i}/{len(chunks)}")

# 2. Quotes
print(f"Pushing {len(arnold_quotes)} quotes...")
for q in arnold_quotes:
    push(q["quote"])

# 3. HR docs, prefix with name so the doc title becomes part of the embedding
print(f"Pushing {len(documents)} HR docs...")
for d in documents:
    push(f"{d['name']}\n{d['content']}")

# 4. GIFs, embed the tags, store the URL in the visible text
print(f"Pushing {len(arnold_gifs)} GIFs...")
for g in arnold_gifs:
    searchable = f"{g['title']} {g['intent']} {' '.join(g['tags'])}"
    visible = f"GIF: {g['title']} | Intent: {g['intent']} | URL: {g['gif_url']}"
    push(visible, searchable=searchable)

print("Done. Knowledge base is loaded.")
