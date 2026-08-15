import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")
    return OpenAI(api_key=api_key)


def _get_vector_db():
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    return QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="learning_rag",
        embedding=embedding_model,
    )


async def process_query(query: str):
    print("Searching Chunks", query)

    vector_db = _get_vector_db()
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
        for result in search_results
    ])

    SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who answers the user query based on the available context retrieved from a PDF file along with page contents and page number.

    You should only answer the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {context}
    """

    openai_client = _get_openai_client()
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    print(f"🤖: {response.choices[0].message.content}")
    return response.choices[0].message.content


