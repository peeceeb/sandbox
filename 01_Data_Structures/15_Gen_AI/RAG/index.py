from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file or environment variables.")

pdf_path = Path(__file__).parent / "nodejs.pdf"
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

# Load the PDF document
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()

# Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
chunks = text_splitter.split_documents(documents=docs)

# Vector embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=api_key)

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
prefer_grpc = os.getenv("QDRANT_PREFER_GRPC", "false").lower() == "true"

try:
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=os.getenv("QDRANT_COLLECTION", "nodejs_docs"),
        url=qdrant_url,
        prefer_grpc=prefer_grpc,
    )
    print(f"Indexed {len(chunks)} chunks into Qdrant at {qdrant_url}")
except Exception as exc:
    raise RuntimeError(
        f"Could not connect to Qdrant at {qdrant_url}. Start Qdrant and confirm it is listening on that URL."
    ) from exc

