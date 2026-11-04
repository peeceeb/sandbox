from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from langchain_core.documents import Document

from rag.Read_GD_Docs import sanitize_documents


def test_sanitize_documents_replaces_surrogates():
    doc = Document(
        page_content="hello" + chr(0xD835) + "world",
        metadata={"title": "bad" + chr(0xD835) + "meta"},
    )

    cleaned = sanitize_documents([doc])[0]

    assert cleaned.page_content == "hello�world"
    assert cleaned.metadata["title"] == "bad�meta"
    assert "\ud835" not in cleaned.page_content
