import os
from typing import Iterable

from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


def sanitize_documents(documents: Iterable[Document]) -> list[Document]:
    cleaned_docs: list[Document] = []
    for doc in documents:
        safe_page_content = doc.page_content.encode("utf-8", errors="replace").decode("utf-8")
        safe_metadata = {}
        for key, value in doc.metadata.items():
            if isinstance(value, str):
                safe_metadata[key] = value.encode("utf-8", errors="replace").decode("utf-8")
            else:
                safe_metadata[key] = value
        cleaned_docs.append(Document(page_content=safe_page_content, metadata=safe_metadata))
    return cleaned_docs


pdf_path = Path(__file__).resolve().parent / "Documents" / "GD_Downloads" / "CRR3_Output_floor_Latest.pdf"
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()
if docs:
    print(docs[0].page_content)
else:
    print("No pages were loaded from the PDF.")


# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400  # Overlap help to maintain context between chunks
)

chunks = text_splitter.split_documents(documents=docs)
cleaned_chunks = sanitize_documents(chunks)


# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

try:
    vector_store = QdrantVectorStore.from_documents(
        documents=cleaned_chunks,
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name="GD_Downloads_Vector"
    )
    print("Indexing of Latest_GD Downloads Completed....")
except Exception as exc:
    print(f"Qdrant connection failed: {exc}")
    print("PDF was loaded and chunked successfully, but vector indexing was skipped.")

