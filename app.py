"""
Arnold fitness bot, Flask backend.

Serves the static chat UI at / and exposes a single /chat endpoint that does
embedding + Cosmos vector retrieval + chat completion.

    python app.py
    -> http://127.0.0.1:5000
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from azure.cosmos import CosmosClient
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "text-embedding-ada-002"
CHAT_MODEL = os.getenv("AZURE_DEPLOYMENT", "gpt-4.1")

# Top-k retrieval from Cosmos. 3 is the sweet spot, bumping to 5 starts
# pulling in semi-relevant chunks that confuse the model on niche questions.
TOP_K = 3

# IMPORTANT: don't change the GIF markdown rule without also checking that
# marked.js on the frontend still renders the image inline. The `!` prefix
# is what flips it from link to embedded image.
SYSTEM_PROMPT = """You are Arnold Schwarzenegger, a no-nonsense fitness coach.

Stay in character at all times. Tough-love approach: blunt when the user is
making excuses, encouraging when they're putting in work. Drop your signature
catchphrases naturally, don't force them.

Rules:
- Open with "Listen up!" or similar to set the tone
- Stick to fitness, training, motivation, and the HR topics in the context
- No politics, religion, or medical advice
- If the context contains a relevant GIF, include it using: ![title](url)
- Keep it punchy. Arnold doesn't ramble.
"""


# --- clients ---
oai = AzureOpenAI(
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
)

cosmos = CosmosClient(os.getenv("COSMOS_ENDPOINT"), os.getenv("COSMOS_KEY"))
container = (
    cosmos.get_database_client("AI_Database")
          .get_container_client("EmbeddingsContainer")
)


app = Flask(__name__, static_folder="static")
CORS(app)


def retrieve(query, k=TOP_K):
    """Return the top-k chunk texts from Cosmos for a query."""
    vec = oai.embeddings.create(input=query, model=EMBED_MODEL).data[0].embedding

    sql = f"""
        SELECT TOP {k} c.text, VectorDistance(c.embedding, @vec) AS score
        FROM c
        ORDER BY VectorDistance(c.embedding, @vec)
    """
    params = [{"name": "@vec", "value": vec}]
    rows = container.query_items(
        query=sql, parameters=params, enable_cross_partition_query=True
    )
    return [r["text"] for r in rows]


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    body    = request.json or {}
    query   = body.get("query", "").strip()
    history = body.get("history", [])  # list of {role, content} from previous turns

    if not query:
        return jsonify({"error": "empty query"}), 400

    try:
        chunks = retrieve(query)
        context = "\n\n".join(chunks)

        user_msg = (
            "Use the context below to answer the question. If the context contains "
            "a relevant GIF, include it in the response.\n\n"
            f"Context:\n---\n{context}\n---\n\n"
            f"Question: {query}"
        )

        # system prompt + previous turns + current question
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += history
        messages += [{"role": "user", "content": user_msg}]

        resp = oai.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.5,
        )
        return jsonify({"response": resp.choices[0].message.content})

    except Exception as e:
        # TODO: hook this up to a real logger, right now errors only surface in the browser
        print(f"[chat error] {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)