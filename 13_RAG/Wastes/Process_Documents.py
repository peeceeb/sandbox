
from pathlib import Path
from itertools import islice
from typing import Iterable, Iterator

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from time import perf_counter

class ProcessDocuments:

    def __init__(self,
        folder_path: str,
        batch_size: int = 100,
        chunk_size: int = 1000,
        chunk_overlap: int = 400
    ):

        self.folder_path = Path(folder_path)
        self.batch_size = batch_size
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

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
        start = perf_counter()
        docs = []
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(str(pdf_file))
                docs.extend(
                    Document(
                        page_content=page.extract_text() or "",
                        metadata={"source": str(pdf_file), "page": page_number},
                    )
                    for page_number, page in enumerate(reader.pages)
                )
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
        
        load_time = perf_counter() - start
        print(f"Loading time: {load_time:.2f}s")
                    
        return docs

    # Step 4: Split documents into chunks
    def split_documents(self,documents: list[Document]) -> list[Document]:
        start = perf_counter()
        chunks = self.text_splitter.split_documents(documents)
        split_time = perf_counter() - start
        print(f"Spliting time: {split_time:.2f}s")
        return chunks

    # Step 5: Sanitize Chunks
    def sanitize_documents(self, documents: Iterable[Document]) -> list[Document]:
            start = perf_counter()
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
            sanitize_time = perf_counter() - start
            print(f"sanitize time: {sanitize_time:.2f}s")
            
            return cleaned_docs




#get_pdf_files()
print("----------------------Process Documents--------------------------")
project_root = Path(__file__).resolve().parent.parent
retrieval = ProcessDocuments(
    folder_path=str(project_root / "documents" / "internal"),
    batch_size=3,
    chunk_size=1000,
    chunk_overlap=400,
)

pdf_files=retrieval.get_pdf_files()

for pdf in pdf_files:
    print(f"Processing PDF: {pdf}/n")


#get_batches
print("-----------------------Process Batches----------------------------")
batches = retrieval.get_batches(retrieval.get_pdf_files())

from pprint import pprint
for i, batch in enumerate(batches, start=1):
    batch_start = perf_counter()
    print(f"Processing Batch {i}:")
    pprint(batch, indent=4, width=100)
    
    print("------------------------Load Documents-----------------------------")
    docs = retrieval.load_documents(batch)
    print(f"Total pages loaded: {len(docs)}\n")
    
    print("------------------------Split Documents----------------------------")
    chunks= retrieval.split_documents(docs)
    print(f"Total Splits Done: {len(chunks)}\n")
    
    print("------------------------Sanitize Documents----------------------------")
    sanitize_chunks= retrieval.sanitize_documents(chunks)
    print(f"Total Splits Sanitized: {len(chunks)}\n")

    batch_time = perf_counter() - batch_start
    print(f"Total batch time: {batch_time:.2f}s\n")
