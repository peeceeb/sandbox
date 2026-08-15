from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

openai_client = OpenAI()

# Lazy globals
_embedding_model = None
_vector_db = None


pdf_path = Path(__file__).parent / "nodejs.pdf"

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents=docs)


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
        _embedding_model = OpenAIEmbeddings(model=model_name)
    return _embedding_model


def get_vector_db():
    """Lazily initialize and return the QdrantVectorStore.

    Raises a RuntimeError with a helpful message if the collection cannot be loaded.
    """
    global _vector_db
    if _vector_db is not None:
        return _vector_db

    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection = os.getenv("RAG_COLLECTION", "learning_rag")

    try:
        _vector_db = QdrantVectorStore.from_existing_collection(
            url=qdrant_url,
            collection_name=collection,
            embedding=_get_embedding_model(),
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize Qdrant collection '{collection}' at {qdrant_url}: {e}\n"
            "Run the create_qdrant_collection script to create the collection and ensure Qdrant is running."
        ) from e

    return _vector_db


def process_query(query: str):
    """Process a text query synchronously for RQ workers.

    This function is synchronous on purpose because RQ executes regular
    functions — async functions return coroutine objects which lead to
    unexpected job results.
    """
    print("Searching Chunks", query)
    vector_db = get_vector_db()
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page_label')}\nFile Location: {result.metadata.get('source')}"
        for result in search_results
    ])

    SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who answers the user query based on the available
    context retrieved from a PDF file (page content, page number, and file location).

    Answer only from the context and point the user to the page number for details.

    Context:
    {context}
    """

    response = openai_client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    answer = response.choices[0].message.content
    print(f"🤖: {answer}")
    return answer


