
from pathlib import Path
from itertools import islice
from typing import Iterable, Iterator

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessDocuments:

    def __init__(self,
        folder_path: str,
        batch_size: int = 100,
        chunk_size: int = 1000,
        chunk_overlap: int = 400):

        self.folder_path = Path(folder_path)
        self.batch_size = batch_size
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)

    # Step 1: Discover PDF files
    def get_pdf_files(self) -> Iterator[Path]:
        return self.folder_path.rglob("*.pdf")

    # Step 2: Divide PDF files into batches
    def get_batches(self, files) -> Iterator[list]:
        while True:
            batch = list(islice(files, self.batch_size))
            if not batch:
                break
            yield batch

    # Step 3: Load PDF documents
    def load_documents(self, pdf_files: list[Path]) -> list[Document]:
        docs = []
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(str(pdf_file))
                documents = loader.load()
                docs.extend(documents)
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
        return docs

    # Step 4: Split documents into chunks
    def split_documents(self,documents: list[Document]) -> list[Document]:
        chunks = self.text_splitter.split_documents(documents)
        return chunks

    # Step 5: Sanitize documents
    def sanitize_documents(self, documents: Iterable[Document]) -> list[Document]:
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

    # Step 6: Process one batch
    def process_batch(self, pdf_files: list[Path]) -> list[Document]:
        docs = self.load_documents(pdf_files)
        chunks = self.split_documents(docs)
        cleaned_chunks = self.sanitize_documents(chunks)
        return cleaned_chunks

    # Step 7: Process all PDFs batch by batch
    def process_all(self):
        pdf_files = self.get_pdf_files()
        for batch_number, batch in enumerate(
            self.get_batches(pdf_files), start=1):
            cleaned_chunks = self.process_batch(batch)
            print(
                f"Batch {batch_number}: "
                f"{len(batch)} PDFs processed | "
                f"{len(cleaned_chunks)} chunks generated"
            )
            yield cleaned_chunks
