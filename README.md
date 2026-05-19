# RAG Clone Arnold Mind

This is a chatbot that answers as Arnold Schwarzenegger. You ask it about training, nutrition, or company HR policies. It answers like Arnold would.

It is not just a prompted GPT wrapper. The model does not know the answers from memory. Before every response, it searches a database of real content. Chunks from Arnold's bodybuilding encyclopedia, his quotes, a set of reaction GIFs, and the company HR documents. It finds the three most relevant pieces and hands them to the model as context. That is what RAG means. The model reads what you give it and answers from there.

## Why this exists

We wanted Arnold to give grounded answers, not hallucinated ones. If you ask "how do I train my shoulders", the model should pull actual text from the book, not invent something that sounds plausible. Retrieval solves that.

## How it works

When you send a message, the backend turns your question into a vector, which is a list of numbers that represents its meaning. It runs that vector against the database and finds the three stored chunks whose vectors are closest to yours. Those chunks become the context. The model reads the context and writes the answer. Arnold is just the costume.

## How to run it

First copy the environment template and fill in your Azure keys.

```
cp .env.example .env
```

Then install the dependencies.

```
pip install -r requirements.txt
```

Then push the knowledge base into Cosmos. This runs once. If you run it again you will get duplicate rows, so do not run it again unless you wipe the container first.

```
python ingest.py
```

Then start the server.

```
python app.py
```

Open `http://127.0.0.1:5000` and start talking to Arnold.

## What is in the repo

`ingest.py` A script you run once before starting the app. It reads the book, splits it into overlapping chunks of 2000 characters, then embeds the chunks plus the quotes, HR docs, and GIFs and writes everything into Cosmos. After that first run it has done its job and you do not touch it again unless you want to add new content to the knowledge base.

`app.py` Starts a Flask server with two routes. The / route serves the HTML file. The /chat route receives a question from the frontend, converts it to a vector, searches Cosmos for the three closest chunks, builds a prompt with that context, sends it to GPT, and returns the answer. That is the entire app. Run it and leave it running.

`static/index.html` is the chat UI. It is a single HTML file with no build step.

`data/` holds the raw knowledge: the book text, the quotes list, the GIFs list, and the HR policy documents. If you want to add something to Arnold's knowledge, add it here and re-run `ingest.py`.

## Stack

Flask serves the backend and the frontend from the same process. Azure OpenAI handles both the embeddings and the chat completions. Azure CosmosDB stores the vectors and runs the similarity search.
