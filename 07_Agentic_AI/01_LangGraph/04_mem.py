from mem0 import Memory
import os
client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


#configuration tells what and how to connect to the different providers for LLM, Embeddings, Graph Store and Vector Store.
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "text-embedding-3-small" }
    },
    "llm": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "gpt-4.1" }
    },
    "graph_store":{
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://ab385712.databases.neo4j.io",
            "username": "neo4j",
            "password": "4Qq7TLVVS27qaQ7O6YPYl6zqLVP2vcXQnPktkgkTGt8"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}
