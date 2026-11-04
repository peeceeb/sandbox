import argparse
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple
from urllib.parse import quote_plus, unquote, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

BASE_URL = "https://www.eba.europa.eu"
SEARCH_URL = f"{BASE_URL}/search"
EBA_PUBLICATIONS_URL = f"{BASE_URL}/publications-and-media/publications"
REGULATORY_BODIES = {
    "EBA": "https://www.eba.europa.eu",
    "EIOPA": "https://www.eiopa.europa.eu",
    "ESMA": "https://www.esma.europa.eu",
}
API_VERSION = "1.0.0"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

ARTICLE_RE = re.compile(r"<article class=\"teaser\".*?</article>", re.IGNORECASE | re.DOTALL)
TITLE_RE = re.compile(
    r"<h4[^>]*teaser__title[^>]*>\s*<a[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"link-icon--tag\"[^>]*>(.*?)</(?:div|span)>", re.IGNORECASE | re.DOTALL)
CALENDAR_RE = re.compile(r"link-icon--calendar\"[^>]*>(.*?)</(?:div|span)>", re.IGNORECASE | re.DOTALL)
DATE_TEXT_RE = re.compile(r"(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{1,2}/\d{1,2}/\d{4})")
STRIP_TAGS_RE = re.compile(r"<[^>]+>")
PUBLICATION_LINK_RE = re.compile(
    r"<h4[^>]*>\s*<a[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)


class PolicyDocument(NamedTuple):
    title: str
    url: str
    doc_type: str
    published_on: datetime
    published_raw: str
    page: int


def api_error(code: str, message: str, status: int):
    return {
        "ok": False,
        "api_version": API_VERSION,
        "error": {
            "code": code,
            "message": message,
        },
    }, status


def parse_args() -> argparse.Namespace:
    default_output_dir = str(Path(__file__).resolve().parent)

    parser = argparse.ArgumentParser(
        description="Fetch latest EBA policy document from EBA search results."
    )
    parser.add_argument("query", nargs="?", help="Search term (example: crr3)")
    parser.add_argument(
        "--regulatory-body",
        default="EBA",
        choices=sorted(REGULATORY_BODIES.keys()),
        help="Regulatory body to search (default: EBA)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=5,
        help="How many search pages to scan (default: 5)",
    )
    parser.add_argument(
        "--strict-keyword",
        action="store_true",
        help="Keep only documents where title or URL contains the query text",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the latest document file",
    )
    parser.add_argument(
        "--output-dir",
        default=default_output_dir,
        help="Directory where the file will be saved when --download is set (default: script directory)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Show top N latest matching documents (default: 3)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Run local API server for frontend integration",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Web host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Web port (default: 8000)",
    )
    return parser.parse_args()


def fetch_html(url: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_text(value: str) -> str:
    text = STRIP_TAGS_RE.sub(" ", value)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_date(date_text: str) -> Optional[datetime]:
    date_text = date_text.strip()
    for fmt in ("%d %B %Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_text, fmt)
        except ValueError:
            continue
    return None


def extract_documents_from_html(html: str, page: int, base_url: str = BASE_URL) -> List[PolicyDocument]:
    documents = []  # type: List[PolicyDocument]

    for article in ARTICLE_RE.findall(html):
        title_match = TITLE_RE.search(article)
        if not title_match:
            continue

        relative_url, title_html = title_match.groups()
        title = clean_text(title_html)
        full_url = urljoin(base_url, unescape(relative_url))

        tag_match = TAG_RE.search(article)
        doc_type = clean_text(tag_match.group(1)) if tag_match else ""

        calendar_match = CALENDAR_RE.search(article)
        calendar_text = clean_text(calendar_match.group(1)) if calendar_match else ""
        date_match = DATE_TEXT_RE.search(calendar_text)
        if not date_match:
            continue

        parsed_date = parse_date(date_match.group(1))
        if not parsed_date:
            continue

        is_document = "document" in doc_type.lower() or "/sites/default/files/" in full_url.lower()
        if not is_document:
            continue

        documents.append(
            PolicyDocument(
                title=title,
                url=full_url,
                doc_type=doc_type or "Document",
                published_on=parsed_date,
                published_raw=date_match.group(1),
                page=page,
            )
        )

    return documents


def extract_documents_from_publications_html(html: str, page: int, base_url: str = BASE_URL) -> List[PolicyDocument]:
    documents = []  # type: List[PolicyDocument]

    for match in PUBLICATION_LINK_RE.finditer(html):
        relative_url, title_html = match.groups()
        full_url = urljoin(base_url, unescape(relative_url))
        lower_url = full_url.lower()

        is_document = (
            "/sites/default/files/" in lower_url
            or lower_url.endswith(".pdf")
            or lower_url.endswith(".doc")
            or lower_url.endswith(".docx")
            or lower_url.endswith(".xls")
            or lower_url.endswith(".xlsx")
            or lower_url.endswith(".zip")
        )
        if not is_document:
            continue

        title = clean_text(title_html)
        if not title or title.lower() == "download document":
            continue

        window_start = max(0, match.start() - 600)
        window_end = min(len(html), match.end() + 1200)
        window_text = clean_text(html[window_start:window_end])
        date_match = DATE_TEXT_RE.search(window_text)
        if not date_match:
            continue

        parsed_date = parse_date(date_match.group(1))
        if not parsed_date:
            continue

        documents.append(
            PolicyDocument(
                title=title,
                url=full_url,
                doc_type="Guidelines",
                published_on=parsed_date,
                published_raw=date_match.group(1),
                page=page,
            )
        )

    return documents


def build_eba_publications_page_url(keyword: str, page: int) -> str:
    params = {
        "text": keyword,
        "document_type": "250",
        "media_topics": "All",
    }
    if page > 0:
        params["page"] = str(page)
    return f"{EBA_PUBLICATIONS_URL}?{urlencode(params)}"


def keyword_in_document(doc: PolicyDocument, keyword: str) -> bool:
    haystack = f"{doc.title} {doc.url}".lower()
    words = [w for w in re.split(r"\s+", keyword.lower().strip()) if w]
    if not words:
        return True
    return all(word in haystack for word in words)


def search_documents(keyword: str, pages: int, timeout: int, regulatory_body: str = "EBA") -> List[PolicyDocument]:
    results = []  # type: List[PolicyDocument]
    base_url = REGULATORY_BODIES.get(regulatory_body.upper(), BASE_URL)
    search_url = f"{base_url}/search"

    for page in range(max(pages, 1)):
        if regulatory_body.upper() == "EBA":
            page_url = build_eba_publications_page_url(keyword, page)
            html = fetch_html(page_url, timeout=timeout)
            results.extend(extract_documents_from_publications_html(html, page=page + 1, base_url=base_url))
        else:
            page_url = f"{search_url}?keys={quote_plus(keyword)}&page={page}"
            html = fetch_html(page_url, timeout=timeout)
            results.extend(extract_documents_from_html(html, page=page + 1, base_url=base_url))

    # Remove duplicates by URL, keeping newest date if repeated.
    dedup = {}  # type: Dict[str, PolicyDocument]
    for doc in results:
        current = dedup.get(doc.url)
        if current is None or doc.published_on > current.published_on:
            dedup[doc.url] = doc

    return list(dedup.values())


def get_matching_documents(keyword: str, pages: int, timeout: int, strict_keyword: bool, regulatory_body: str = "EBA") -> Tuple[List[PolicyDocument], List[PolicyDocument], List[PolicyDocument]]:
    docs = search_documents(keyword, pages, timeout, regulatory_body=regulatory_body)
    strict_docs = [doc for doc in docs if keyword_in_document(doc, keyword)]
    matching_docs = strict_docs if (strict_keyword and strict_docs) else docs
    matching_docs.sort(key=lambda d: d.published_on, reverse=True)
    return docs, strict_docs, matching_docs


def pick_filename(url: str) -> str:
    name = Path(unquote(urlparse(url).path)).name
    if not name:
        return "eba_document.bin"
    return name


def download_file(url: str, output_dir: Path, timeout: int) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / pick_filename(url)

    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as response:
        content = response.read()
    target.write_bytes(content)
    return target


def documents_to_json(docs: List[PolicyDocument], top_n: int = 3) -> List[Dict[str, str]]:
    output = []
    for doc in docs[: max(top_n, 1)]:
        output.append(
            {
                "title": doc.title,
                "url": doc.url,
                "download_url": doc.url,
                "doc_type": doc.doc_type,
                "published_on": doc.published_raw,
                "page": str(doc.page),
            }
        )
    return output


def run_web_server(args: argparse.Namespace) -> int:
    try:
        from flask import Flask, jsonify, request
    except Exception:
        print("Flask is required for web mode. Install with: pip install flask")
        return 1

    app = Flask(__name__)
    @app.route("/", methods=["GET"])
    def root():
        return jsonify(
            {
                "message": "Policy Fetch API server is running",
                "api_version": API_VERSION,
                "spec_url": "/api/spec",
                "policies_url": "/api/policies",
            }
        )

    @app.route("/api/policies", methods=["GET", "POST"])
    def api_policies():
        def parse_bool(value: object) -> bool:
            return str(value).strip().lower() in {"1", "true", "yes", "on"}

        if request.method == "GET":
            regulatory_body = (request.args.get("regulatory_body") or args.regulatory_body).strip().upper()
            query = (request.args.get("query") or "").strip()
            strict_keyword = parse_bool(request.args.get("strict_keyword") or "false")
            pages_raw = request.args.get("pages")
            timeout_raw = request.args.get("timeout")
        else:
            payload = request.get_json(silent=True) or {}
            regulatory_body = str(payload.get("regulatory_body") or args.regulatory_body).strip().upper()
            query = str(payload.get("query") or "").strip()
            strict_keyword = parse_bool(payload.get("strict_keyword", False))
            pages_raw = payload.get("pages")
            timeout_raw = payload.get("timeout")

        if regulatory_body not in REGULATORY_BODIES:
            body, status = api_error(
                "UNSUPPORTED_REGULATORY_BODY",
                f"Unsupported regulatory_body: {regulatory_body}. Allowed: {', '.join(sorted(REGULATORY_BODIES.keys()))}",
                400,
            )
            return jsonify(body), status

        try:
            pages = max(int(pages_raw) if pages_raw is not None else args.pages, 1)
            timeout = max(int(timeout_raw) if timeout_raw is not None else args.timeout, 1)
        except ValueError:
            body, status = api_error("INVALID_NUMERIC_INPUT", "pages and timeout must be integers", 400)
            return jsonify(body), status

        try:
            docs, strict_docs, matching_docs = get_matching_documents(
                query,
                pages,
                timeout,
                strict_keyword,
                regulatory_body=regulatory_body,
            )

            top_docs = documents_to_json(matching_docs, top_n=3)
            return jsonify(
                {
                    "ok": True,
                    "api_version": API_VERSION,
                    "regulatory_body": regulatory_body,
                    "query": query,
                    "pages": pages,
                    "timeout": timeout,
                    "strict_keyword": strict_keyword,
                    "total_documents": len(docs),
                    "strict_matches": len(strict_docs),
                    "top_documents": top_docs,
                }
            )
        except Exception as exc:
            body, status = api_error("FETCH_FAILED", str(exc), 500)
            return jsonify(body), status

    @app.route("/api/spec", methods=["GET"])
    def api_spec():
        return jsonify(
            {
                "api_name": "Policy Fetch API",
                "api_version": API_VERSION,
                "endpoints": {
                    "policies": {
                        "path": "/api/policies",
                        "methods": ["GET", "POST"],
                        "request": {
                            "regulatory_body": sorted(REGULATORY_BODIES.keys()),
                            "query": "string (optional, default='')",
                            "strict_keyword": "boolean (optional, default=false)",
                            "pages": "integer >= 1 (optional)",
                            "timeout": "integer >= 1 (optional)",
                        },
                        "response": {
                            "ok": "boolean",
                            "api_version": "string",
                            "regulatory_body": "string",
                            "query": "string",
                            "pages": "integer",
                            "timeout": "integer",
                            "strict_keyword": "boolean",
                            "total_documents": "integer",
                            "strict_matches": "integer",
                            "top_documents": [
                                {
                                    "title": "string",
                                    "url": "string",
                                    "download_url": "string",
                                    "doc_type": "string",
                                    "published_on": "string",
                                    "page": "string",
                                }
                            ],
                        },
                        "errors": [
                            "UNSUPPORTED_REGULATORY_BODY",
                            "INVALID_NUMERIC_INPUT",
                            "FETCH_FAILED",
                        ],
                    }
                },
            }
        )

    print(f"Starting API server at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)
    return 0


def run_cli(args: argparse.Namespace) -> int:
    query = (args.query or "").strip()

    try:
        docs, strict_docs, matching_docs = get_matching_documents(
            query,
            args.pages,
            args.timeout,
            args.strict_keyword,
            regulatory_body=args.regulatory_body,
        )
    except Exception as exc:
        print(f"Failed to query EBA website: {exc}")
        return 1

    if not docs:
        print("No document results were found.")
        return 0

    print(f"Found {len(docs)} document results across {max(args.pages, 1)} page(s).")
    if args.strict_keyword:
        print(f"Strict keyword matches: {len(strict_docs)}")

    top_n = max(args.top, 1)
    print("\nTop latest documents:")
    for index, doc in enumerate(matching_docs[:top_n], start=1):
        print(f"{index}. {doc.title}")
        print(f"   Date: {doc.published_raw}")
        print(f"   Type: {doc.doc_type}")
        print(f"   URL : {doc.url}")

    latest = matching_docs[0]
    print("Latest selected document:")
    print(f"- Title: {latest.title}")
    print(f"- Date : {latest.published_raw}")
    print(f"- URL  : {latest.url}")

    if args.download:
        try:
            saved_path = download_file(latest.url, Path(args.output_dir).expanduser().resolve(), args.timeout)
            print(f"\nDownloaded to: {saved_path}")
        except Exception as exc:
            print(f"Download failed: {exc}")
            return 1
    else:
        print("\nDownload not started. Use --download to save the latest document.")

    return 0


def main() -> int:
    args = parse_args()
    if args.web:
        return run_web_server(args)
    return run_cli(args)

def get_latest_docs():
    # Hardcoded values for the search
    hardcoded_keyword = ""              # e.g., "CRR3", "IFRS", or empty for general
    hardcoded_pages = 2                 # Number of search pages to scan
    hardcoded_timeout = 30              # HTTP timeout in seconds
    hardcoded_strict_keyword = False    # Whether to enforce strict keyword matching
    hardcoded_regulatory_body = "EBA"   # Regulatory body (e.g., "EBA", "EIOPA", "ESMA")
    hardcoded_top_n = 5                 # Number of top latest documents to return

    try:
        _, _, matching = get_matching_documents(
            keyword=hardcoded_keyword,
            pages=hardcoded_pages,
            timeout=hardcoded_timeout,
            strict_keyword=hardcoded_strict_keyword,
            regulatory_body=hardcoded_regulatory_body,
        )
    except Exception as exc:
        print(f"[get_latest_docs] fetch failed: {exc}")
        return []

    # Use the hardcoded_top_n for slicing
    return [doc.url for doc in matching[:hardcoded_top_n]]

if __name__ == "__main__":
    raise SystemExit(main())
