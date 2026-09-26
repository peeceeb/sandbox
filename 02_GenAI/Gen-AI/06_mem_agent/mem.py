from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time

from neo4j import GraphDatabase
from ollama import Client

os.environ.setdefault("MEM0_TELEMETRY", "false")

from mem0 import Memory

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

NEO4J_URI = os.getenv("NEO4J_URI") or os.getenv("NEO_CONNECTION_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") or os.getenv("NEO_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") or os.getenv("NEO_PASSWORD")

if not NEO4J_URI or not NEO4J_PASSWORD:
    raise RuntimeError("Set NEO4J_URI/NEO_CONNECTION_URI and NEO4J_PASSWORD/NEO_PASSWORD in .env before starting the app.")

ollama_client = Client(host=OLLAMA_BASE_URL)

def ensure_model(model_name: str):
    models = ollama_client.list().get("models", [])
    names = []
    for model in models:
        names.append(model.get("name") or model.get("model"))
    short_name = model_name.split(":")[0]
    if not any(name and name.split(":")[0] == short_name for name in names):
        raise RuntimeError(
            f"Ollama model '{model_name}' is not installed. Run: ollama pull {short_name}"
        )

ensure_model(OLLAMA_MODEL)
ensure_model(OLLAMA_EMBED_MODEL)

graph_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": OLLAMA_EMBED_MODEL,
            "ollama_base_url": OLLAMA_BASE_URL,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": OLLAMA_MODEL,
            "ollama_base_url": OLLAMA_BASE_URL,
            "temperature": 0.1,
            "max_tokens": 256,
        },
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URI,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD,
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "mem0_ollama_768",
            "embedding_model_dims": 768,
        },
    },
}

mem_client = Memory.from_config(config)
persistence_executor = ThreadPoolEx765r43f
    prompt = (
        "Extract durable facts from this conversation as JSON. "
        "Return only a JSON array of objects with string fields "
        "subject, relation, and object. Use an empty array when there "
        "are no durable facts.\n\n"
        f"Conversation:\n{text}"
    )
    raw = ollama_generate(prompt, system_prompt="You are a strict JSON extractor.")
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("` ")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("[")
        end = cleaned.rfind("]")
        if start != -1 and end != -1 and end > start:
            return json.loads(cleaned[start : end + 1])
        return []


def save_graph_facts(user_id: str, facts):
    if not facts:
        return
    query = """
    MERGE (user:User {id: $user_id})
    WITH user, $facts AS facts
    UNWIND facts AS fact
    MERGE (subject:Entity {name: fact.subject})
    MERGE (object:Entity {name: fact.object})
    MERGE (user)-[:MENTIONS]->(subject)
    MERGE (user)-[:MENTIONS]->(object)
    MERGE (subject)-[relationship:RELATES_TO]->(object)
    SET relationship.type = fact.relation
    """
    with graph_driver.session(database="neo4j") as session:
        session.run(query, user_id=user_id, facts=facts).consume()


def persist_memory_and_graph(user_query: str, ai_response: str):
    persistence_start = time.perf_counter()
    memory_start = time.perf_counter()
    try:
        mem_client.add(
            user_id="Michael_Jackson",
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": ai_response},
            ],
            infer=False,
        )
        print(f"Vector memory save time: {time.perf_counter() - memory_start:.2f} seconds")

        facts_start = time.perf_counter()
        graph_facts = extract_graph_facts(f"User: {user_query}\nAssistant: {ai_response}")
        print(f"Graph fact extraction time: {time.perf_counter() - facts_start:.2f} seconds")

        graph_write_start = time.perf_counter()
        save_graph_facts("Michael_Jackson", graph_facts)
        print(f"Neo4j graph write time: {time.perf_counter() - graph_write_start:.2f} seconds")
        print("Loaded facts into Graphs")
    except Exception as error:
        print(f"Graph/memory persistence failed: {type(error).__name__}: {error}")
    print(f"Graph/memory save time: {time.perf_counter() - persistence_start:.2f} seconds")


while True:
    user_query = input("> ")

    search_memory = mem_client.search(
        query=user_query,
        filters={"user_id": "Michael_Jackson"},
        top_k=5,
    )

    memories = [
        f"ID: {mem.get('id')}  Memory: {mem.get('memory')}"
        for mem in search_memory.get("results")
    ]

    print("Found Memories", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    try:
        ai_start = time.perf_counter()
        ai_response = ollama_generate(
            f"{SYSTEM_PROMPT}\nUser: {user_query}",
            system_prompt="You are a helpful assistant. Answer clearly and briefly.",
        )
        ai_elapsed = time.perf_counter() - ai_start
    except Exception:
        ai_elapsed = time.perf_counter() - ai_start
        ai_response = "Ollama model is not available or not responding. Stored memories: " + "; ".join(memories)

    print("AI:", ai_response)
    print(f"AI response time: {ai_elapsed:.2f} seconds")

    if not ai_response.startswith("Ollama model is not available"):
        persistence_executor.submit(persist_memory_and_graph, user_query, ai_response)
        print("Memory persistence queued in background...")




