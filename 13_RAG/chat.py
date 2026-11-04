import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()


# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db_download = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="GD_Downloads_Vector",
    embedding=embedding_model,
)

vector_db_document = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="GD_Docs_Vector",
    embedding=embedding_model,
)

vector_csv_metadata= QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="CSV_Metadata_Vector",
    embedding=embedding_model,
)

# Take user input from command line argument or interactive input
if len(sys.argv) > 1:
    user_query = sys.argv[1]
else:
    user_query = input("Ask something: ")

# Relevant chunks from the vector db
search_results_GD_download = vector_db_download.similarity_search(query=user_query)
search_results_GD_document = vector_db_document.similarity_search(query=user_query)
search_results_csv_metadata = vector_csv_metadata.similarity_search(query=user_query)


def build_context(results, collection_name):
    if not results:
        return f"No relevant passages were found in {collection_name}."

    pages = {}
    for result in results:
        metadata = getattr(result, "metadata", {}) or {}
        page_content = getattr(result, "page_content", "") or ""
        page_label = metadata.get("page_label", "unknown")
        source = metadata.get("source", "unknown")

        page_key = (source, str(page_label))
        if page_key not in pages:
            pages[page_key] = []
        if page_content.strip():
            pages[page_key].append(page_content.strip())

    parts = []
    for page_number, ((source, page_label), page_contents) in enumerate(pages.items(), 1):
        parts.append(
            f"Page {page_number}:\n"
            f"- Source: {source}\n"
            f"- Page label: {page_label}\n"
            f"- Content:\n{' '.join(page_contents)}"
        )

    return "\n\n".join(parts)


context_document = build_context(search_results_GD_document, "GD_Documents")
print(f"Context from GD_Documents:\n{context_document}\n")
context_download = build_context(search_results_GD_download, "GD_Downloads")
print(f"Context from GD_Downloads:\n{context_download}\n")
context_metadata = build_context(search_results_csv_metadata, "CSV_Metadata")
print(f"Context from CSV_Metadata:\n{context_metadata}\n")

SYSTEM_PROMPT = f"""
You are an AI assistant that compares two sets of retrieved document context.

Your job:
1. Compare Context 1 Context 2 and Context 3.
2. Identify the key differences between them.
3. Highlight what information is present in Context 2 but missing from Context 1.
4. Answer the user's question and summarize the findings from the comparison in layman's terms.
6. If the answer is not supported by the context, say: "This information is out of scope."

Important rules:
- Use the retrieved content as evidence.
- Mention page numbers and file locations when available.
- Be concise but clear.
- Prefer a structured response such as:
  - Similarities
  - Differences
  - Best answer to the user's query

Context 1 (GD_Documents):
{context_document}

Context 2 (GD_Downloads):
{context_download}

Context 3 (CSV_Metadata):
{context_metadata}
"""

response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]
)

response_text = response.choices[0].message.content or ""
print(f"🤖: {response_text}")

txt_dir = Path(__file__).resolve().parent / "TXT_Generated"
txt_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
txt_file = txt_dir / f"response_{timestamp}.txt"


txt_file = txt_dir / f"response_{timestamp}.txt"
txt_file.write_text(response_text, encoding="utf-8")
print(f"Text document saved at: {txt_file}")
