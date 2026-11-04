
import streamlit as st
import eba_policy_fetcher_2
from datetime import datetime
from fpdf import FPDF
import base64
import time
import streamlit.components.v1 as components
import sys
from pathlib import Path 
import os
import subprocess
import unicodedata
import re


st.set_page_config(page_title="DRAFT Generator", layout="wide", page_icon="🏦")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    header[data-testid="stHeader"] { height: 0rem; }

    /* Gradient animated title banner */
    .hero {
        background: linear-gradient(-45deg, #0b3d91, #1e6091, #168aad, #34a0a4);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        padding: 22px 28px;
        border-radius: 16px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .hero h1 { margin: 0; font-size: 2rem; }
    .hero p { margin: 4px 0 0; opacity: 0.9; }

    /* Glass metric cards */
    .metric-card {
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 14px;
        padding: 14px 16px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.12);
    }
    .metric-num { font-size: 1.6rem; font-weight: 700; color: #0b3d91; }
    .metric-lbl { font-size: 0.8rem; color: #555; text-transform: uppercase; letter-spacing: 1px; }

    /* Status badge */
    .badge-ok { background:#d8f3dc; color:#1b4332; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600;}
    .badge-wait { background:#ffe5d9; color:#9d0208; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600;}

    /* ---- Scroll reveal animations ---- */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(40px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    /* Each reveal block animates as it enters the viewport (scroll-driven) */
    .reveal {
        animation: fadeUp 0.9s ease both;
        animation-timeline: view();
        animation-range: entry 0% cover 30%;
    }
    /* PDF viewer gets a soft zoom-in as you scroll to it */
    .pdf-frame {
        animation: fadeIn 1s ease both;
        animation-timeline: view();
        animation-range: entry 0% cover 10%;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    .pdf-frame:hover {
        transform: scale(1.03);
        box-shadow: 0 40px 100px rgba(0,0,0,0.22);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Session State ----------------

if "brd" not in st.session_state:
    st.session_state.brd = ""
if "hitl_notes" not in st.session_state:
    st.session_state.hitl_notes = []
if "show_pdf" not in st.session_state:
    st.session_state.show_pdf = False
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "chosen_link" not in st.session_state:
    st.session_state.chosen_link = None  
if "doc_links" not in st.session_state:
    st.session_state.doc_links = []
if "downloaded_link" not in st.session_state:
    st.session_state.downloaded_link = None
if "downloaded_pdf_path" not in st.session_state:
    st.session_state.downloaded_pdf_path = None
if "picked_idx" not in st.session_state:
    st.session_state.picked_idx = None
   

st.sidebar.write("DEBUG:", st.session_state)


PDF_GEN_DIRS = [
    Path(r"C:\Users\User\Desktop\ARC\rag\PDF_Generated"),
    Path(__file__).resolve().parent / "PDF_Generated"
]


from urllib.parse import unquote, urlparse


def parse_filename_from_url(url: str) -> str:
    if not url:
        return "Document"
    name = Path(unquote(urlparse(url).path)).name
    if name:
        return name
    return url.rstrip("/").split("/")[-1] or "Document"


def handle_selected_pdf_download(chosen_link: str):
    """
    Downloads chosen_link into PDF_GEN_DIRS.
    - If chosen_link is different from previous st.session_state.downloaded_link:
      deletes existing downloaded PDFs from target folders and downloads the newly chosen link.
    - If chosen_link is the same and file exists:
      reuses existing downloaded PDF without downloading again.
    """
    prev_link = st.session_state.get("downloaded_link")
    link_changed = (prev_link != chosen_link)

    for gen_dir in PDF_GEN_DIRS:
        gen_dir.mkdir(parents=True, exist_ok=True)

    primary_dir = PDF_GEN_DIRS[0]
    existing_pdfs = [f for f in primary_dir.glob("*.*") if f.is_file() and not f.name.startswith("DRAFT_")]

    if link_changed or not existing_pdfs:
        # Delete existing downloaded document PDFs from all target folders
        for gen_dir in PDF_GEN_DIRS:
            for old_file in gen_dir.glob("*.*"):
                if old_file.is_file() and not old_file.name.startswith("DRAFT_"):
                    try:
                        old_file.unlink()
                    except Exception as e:
                        print(f"Warning: Failed to delete {old_file}: {e}")

        with st.spinner("📥 Downloading selected document PDF..."):
            try:
                saved_path = eba_policy_fetcher_2.download_file(chosen_link, primary_dir, timeout=30)
                st.session_state.downloaded_link = chosen_link
                st.session_state.downloaded_pdf_path = str(saved_path)

                # Also sync copy to secondary PDF_Generated directory if different
                proj_dir = PDF_GEN_DIRS[1]
                if proj_dir.resolve() != primary_dir.resolve():
                    proj_dir.mkdir(parents=True, exist_ok=True)
                    (proj_dir / saved_path.name).write_bytes(saved_path.read_bytes())
            except Exception as exc:
                st.error(f"Failed to download selected PDF document: {exc}")
    else:
        st.session_state.downloaded_link = chosen_link


def scroll_down():
    """Fallback: jump to an anchor placed lower on the page."""
    st.markdown(f"<div id='scroll-target-{time.time()}'></div>", unsafe_allow_html=True)
    components.html(
        f"""
        <script>
            const el = window.parent.document.querySelector('[id^="scroll-target"]');
            if (el) el.scrollIntoView({{behavior:'smooth', block:'center'}});
        </script>
        """,
        height=0,
    )

def safe_str(text: str) -> str:
    """Sanitize text for FPDF latin-1 rendering: replace emojis, smart quotes, normalize unicode."""
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
        "\u2022": "*", "\u25aa": "*", "\u2026": "...", "\u2122": "TM", "\u00ae": "(R)", "\u00a9": "(C)",
        "\u2033": '"', "\u2032": "'", "\u00ab": '"', "\u00bb": '"',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Strip all remaining emoji / non-BMP characters
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    # Strip common emoji in BMP range
    text = re.sub(r'[\u2600-\u27bf\ufe0f\u200d]', '', text)
    normalized = unicodedata.normalize('NFKD', text)
    return normalized.encode('latin-1', errors='replace').decode('latin-1')

                                                   
                                                 
                         
                                                            

class ExecutiveBRDPDF(FPDF):
    """Custom FPDF subclass with professional header banner and page footer."""
    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(11, 61, 145)  # Navy banner
            self.rect(0, 0, 210, 26, 'F')
            self.set_font('Helvetica', 'B', 14)
            self.set_text_color(255, 255, 255)
            self.set_xy(15, 5)
            self.cell(0, 7, safe_str('BUSINESS REQUIREMENT DOCUMENT (DRAFT)'), ln=True)
            self.set_font('Helvetica', '', 9)
            self.set_text_color(200, 225, 255)
            self.set_x(15)
            self.cell(0, 5, safe_str('AI Regulatory Companion - Automated RAG Analysis Report'), ln=True)
            self.ln(6)
        else:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, safe_str('Business Requirement Document (DRAFT) - AI Regulatory Companion'), ln=True)
            self.set_draw_color(220, 220, 220)
            self.line(15, 12, 195, 12)
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, safe_str(f'Page {self.page_no()}'), align='C')


def render_markdown_table(pdf, table_lines):
    """Render markdown table lines as a formatted PDF table with shaded header row and alternating rows."""
    parsed_rows = []
    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.match(r"^:?-+:?$", c) for c in cells):
            continue
        parsed_rows.append(cells)

    if not parsed_rows:
        return

    num_cols = max(len(row) for row in parsed_rows)
    avail_width = 180.0
    col_width = avail_width / num_cols

    for row_idx, row in enumerate(parsed_rows):
        if row_idx == 0:
            pdf.set_fill_color(11, 61, 145)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 9)
        else:
            if row_idx % 2 == 1:
                pdf.set_fill_color(245, 247, 250)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(40, 40, 40)
            pdf.set_font("Helvetica", "", 9)

        pdf.set_draw_color(210, 215, 220)

        while len(row) < num_cols:
            row.append("")

        for cell in row:
            clean_cell = safe_str(cell.replace("**", "").replace("*", ""))
            pdf.cell(col_width, 7, clean_cell, border=1, align="L", fill=True)
        pdf.ln()

    pdf.ln(4)


def make_pdf_bytes(text: str) -> bytes:
    """Generate a professionally formatted Executive DRAFT PDF from markdown-style text."""
    pdf = ExecutiveBRDPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # Standardize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")

    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # --- Markdown Table ---
        if "|" in line and line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            render_markdown_table(pdf, table_lines)
            continue

        # --- Horizontal Divider ---
        if line.strip() in ("---", "***", "___"):
            pdf.set_draw_color(210, 220, 230)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)
            i += 1
            continue

        # --- Empty Line ---
        if not line.strip():
            pdf.ln(3)
            i += 1
            continue

        # --- Callout Section Headers ---
        upper_line = line.upper()
        if "HUMAN-IN-THE-LOOP" in upper_line or "RAG ANALYSIS" in upper_line:
            pdf.set_fill_color(235, 243, 250)
            pdf.set_draw_color(52, 160, 164)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(11, 61, 145)
            clean_label = safe_str(line.replace("####", "").replace("###", "").replace("##", "").replace("#", "").replace("&", "&").strip())
            y_start = pdf.get_y()
            pdf.rect(15, y_start, 180, 9, 'F')
            # Left teal accent bar
            pdf.set_fill_color(52, 160, 164)
            pdf.rect(15, y_start, 3, 9, 'F')
            pdf.set_xy(21, y_start + 1)
            pdf.cell(0, 7, clean_label, ln=True)
            pdf.ln(3)
            i += 1
            continue

        # --- Headers ---
        if line.startswith("#"):
            header_level = len(line) - len(line.lstrip("#"))
            header_text = safe_str(line.lstrip("#").strip())

            if header_level <= 2:
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(11, 61, 145)
                pdf.ln(3)
                pdf.multi_cell(0, 6, header_text)
                pdf.set_draw_color(52, 160, 164)
                pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                pdf.ln(3)
            else:
                pdf.set_font("Helvetica", "B", 10.5)
                pdf.set_text_color(30, 96, 145)
                pdf.ln(2)
                pdf.multi_cell(0, 5, header_text)
                pdf.ln(1)
            i += 1
            continue

        # --- Numbered List Items ---
        numbered_match = re.match(r"^\s*(\d+)\.\s+(.*)", line)
        if numbered_match:
            num_label = numbered_match.group(1) + "."
            item_content = safe_str(numbered_match.group(2).replace("**", ""))
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(11, 61, 145)
            pdf.set_x(20)
            pdf.cell(8, 5, num_label, ln=False)
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, item_content)
            i += 1
            continue

        # --- Bullet Points ---
        if line.lstrip().startswith(("- ", "* ")):
            bullet_content = safe_str(re.sub(r"^\s*[-*]\s*", "", line).replace("**", ""))
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(50, 50, 50)
            pdf.set_x(20)
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(52, 160, 164)
            pdf.cell(5, 5, safe_str("\xb7"), ln=False)  # middle dot
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, bullet_content)
            i += 1
            continue

        # --- Regular Body Text ---
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(40, 40, 40)
        clean_body = safe_str(line.replace("**", ""))
        pdf.multi_cell(0, 5, clean_body)
        i += 1

    # Export PDF bytes safely
    try:
        out = pdf.output(dest="S")
    except TypeError:
        out = pdf.output()

    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    elif isinstance(out, str):
        return out.encode("latin-1", errors="replace")
    return bytes(out)


def build_brd(params: dict):
    def val(x):
        return x if x else "N/A"

    notes = params.get("hitl_notes", [])
    if notes:                       
        lines = []                  
        for n in notes:             
            lines.append(f"- {n}")  
        notes_md = "\n".join(lines) 
    else:
        notes_md = "N/A"
    
     
    return f"""Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

#### PARAMETERS PASSED
| Parameter | Value |
|-----------|-------|
| Country | {val(params['country'])} |
| Regulatory Body | {val(params['body'])} |
| Regulation Topic | {val(params['topic'])} |
                                             


#### HUMAN-IN-THE-LOOP INPUT
{notes_md}"""


st.markdown("""
    <div class="hero">
        <h1>🏦 AI Regulatory Companion</h1>
    </div>
""", unsafe_allow_html=True)


c1, c2 = st.columns([1, 2])

st.markdown("""
    
    <style>
    /* Vertical divider line positioned at ~1/3 width (between c1 and c2) */
    .divider-line {
        position: fixed;
        top: 150px;                /* start 100px lower (below the hero banner) */
        left: 35.00%;
        width: 3px;
        height: calc(100vh - 200px);   /* shorten: 100px off top + 100px off bottom */
        background: linear-gradient(
            to bottom,
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.8) 20%,
            rgba(255,255,255,0.8) 80%,
            rgba(255,255,255,0) 100%
        );
        z-index: 999;
        pointer-events: none;      /* clicks pass through */
    }

    /* Glowing circle fixed at vertical center — does NOT move on scroll */
    .divider-dot {
        position: fixed;
        top: 50%;
        left: 35.07%;
        transform: translate(-50%, -50%);
        width: 12px;               /* 80% of 16px */
        height: 12px;              /* 80% of 16px */
        border-radius: 50%;
        background: rgba(255,255,255,0.8);   /* 80% brightness */
        box-shadow:
            0 0 8px rgba(255,255,255,0.7),
            0 0 18px rgba(255,255,255,0.55),
            0 0 30px rgba(52,160,164,0.48);  /* teal glow at 80% */
        z-index: 1000;
        pointer-events: none;
        animation: pulseGlow 2.5s ease-in-out infinite;
    }

    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 8px rgba(255,255,255,0.9),    /* 👈 raise these */
                        0 0 18px rgba(255,255,255,0.75),
                        0 0 30px rgba(52,160,164,0.6);
        }
        50% {
            box-shadow: 0 0 12px rgba(255,255,255,1),      /* 👈 and these */
                        0 0 26px rgba(255,255,255,0.9),
                        0 0 45px rgba(52,160,164,0.9);
        }
    }
    </style>

    <div class="divider-line"></div>
    <div class="divider-dot"></div>
""", unsafe_allow_html=True)


with c1:
    st.subheader("⚙️ Parameters")
    na = lambda x: "N/A" if x == "" else x

    country = st.selectbox("🌍 Country",
                            ["", "Germany"],
                            format_func=na)
    R_body = st.selectbox("🏛️ Regulatory Body",
                            ["", "EBA", "EIOPA", "ESMA"],
                            format_func=na)
    R_topic = st.selectbox("📚 Regulation Topic",
                            ["", "CRR3"],
                            format_func=na)
                                                   
                                                                                   
                                           
    #S_clause = st.selectbox("📄 Specific Clause",
    #                       ["", "Article 123 (Retail)", "Article 124 (Property)"],
    #                         format_func=na)
    duration = st.selectbox("⏱️ Duration",
                            [3, 6],                                 
                            format_func=lambda x: f"last {x} Months")



# ---------- BUTTON 1: Get Latest Doc ----------

    if st.button("📥 Get Latest Doc", use_container_width=True, type="primary"):
        if not any([country, R_body, R_topic, duration]):
            st.warning("⚠️ Please fill all 5 parameters first.")
        else:
            with st.spinner("🔎 Fetching latest documents..."):
                st.session_state.doc_links = eba_policy_fetcher_2.get_latest_docs()
                st.session_state.chosen_link = None
                st.session_state.picked_idx = None
        scroll_down()
    st.divider()

# ---------- Show 5 links with radio + view buttons ----------

    if st.session_state.doc_links:
        st.subheader("🔗 Choose Document")

        if (
            "picked_idx" not in st.session_state
            or st.session_state.picked_idx is None
            or not isinstance(st.session_state.picked_idx, int)
            or st.session_state.picked_idx >= len(st.session_state.doc_links)
        ):
            st.session_state.picked_idx = None

        st.markdown("""
            <style>
            /* Custom professional styling for document row selection buttons */
            div[data-testid="stButton"] button {
                text-align: left !important;
                justify-content: flex-start !important;
             
                                                                      
                                                         
                                                           
                padding: 12px 16px !important;
                min-height: 52px !important;
                height: auto !important;
                white-space: normal !important;
                word-break: break-word !important;
                line-height: 1.4 !important;
                border-radius: 12px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        for idx, link in enumerate(st.session_state.doc_links):
            filename = parse_filename_from_url(link)
            is_selected = (st.session_state.picked_idx == idx)
            radio_icon = "🔘" if is_selected else "⚪"
            btn_type = "primary" if is_selected else "secondary"

            # Row container with 3.5:1 column ratio guaranteeing 1-to-1 vertical alignment
            row_left, row_right = st.columns([3.5, 1])
                              
                                       
                        
                           
                                                     
             
                                  
                                                                                 
                             

            with row_left:
                if st.button(
                    f"{radio_icon} Doc {idx + 1}: {filename}",
                    key=f"doc_sel_btn_{idx}",
                    use_container_width=True,
                    type=btn_type,
                ):
                    st.session_state.picked_idx = idx
                    st.session_state.chosen_link = link
                    scroll_down()
                    st.rerun()

            with row_right:
                st.link_button("🔎 View", link, use_container_width=True)

        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        st.subheader("💬 Human-in-the-Loop")

        hitl_notes = st.text_area("✏️ Provide Topic of interest")

                        
                                                                            

    st.divider()


    # ---------- BUTTON 2: Generate BRD (only after a choice) ----------

    if st.session_state.chosen_link:
        if st.button("🚀 Generate DRAFT", use_container_width=True, type="primary"):
            with st.spinner("🧠 Executing RAG & Generating DRAFT..."):
                # 1. Download/reuse selected document PDF (deletes prior PDF if link changed)
                                           
                                       
                                         
                                           
                                                                                    
                                                                  
                  
                handle_selected_pdf_download(st.session_state.chosen_link)
                                            
                         
             
                                                                                     

                chat_script = Path(__file__).resolve().parent / "chat.py"
                
                # Setup UTF-8 environment for subprocess execution
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"
                
                try:
                    # 2. Run chat.py passing hitl_notes as argv[1] (assigned to user_query)
                    query_text = hitl_notes.strip() if hitl_notes and hitl_notes.strip() else "General Regulation Overview"
                    result = subprocess.run(
                        [sys.executable, str(chat_script), query_text],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        env=env,
                        timeout=90  # Timeout for vector search + LLM generation
                    )

                    if result.returncode != 0:
                        st.error(f"Error running chat.py: {result.stderr}")
                    else:
                        # 3. Extract LLM response output from stdout
                        llm_output = result.stdout.strip()
                        
                        # 4. Build DRAFT document text incorporating the LLM output
                        brd_content = f"""Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

#### PARAMETERS PASSED
| Parameter | Value |
|-----------|-------|
| Country | {country if country else "N/A"} |
| Regulatory Body | {R_body if R_body else "N/A"} |
| Regulation Topic | {R_topic if R_topic else "N/A"} |
| Selected Link | {st.session_state.chosen_link} |

#### HUMAN-IN-THE-LOOP INPUT (QUERY)
{query_text}

---
#### RAG ANALYSIS & LLM RESPONSE
{llm_output}
"""
                        # 5. Save to session state and convert to safe PDF bytes
                        st.session_state.brd = brd_content
                        st.session_state.pdf_bytes = make_pdf_bytes(st.session_state.brd)
                             
                           

                        # 6. Save generated BRD PDF to PDF_GEN_DIRS
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        for gen_dir in PDF_GEN_DIRS:
                            gen_dir.mkdir(parents=True, exist_ok=True)
                            brd_pdf_path = gen_dir / f"DRAFT_{timestamp}.pdf"
                            brd_pdf_path.write_bytes(st.session_state.pdf_bytes)
                                        

                        st.success("✅ DRAFT successfully generated from RAG output!")
                        scroll_down()

                except subprocess.TimeoutExpired:
                    st.error("Chat script execution timed out (90s limit).")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("👆 Pick one document above to enable DRAFT generation.")     

   


with c2:

    if st.session_state.brd:

        # ----- Animated metric cards -----

        params_count = 0
        if country:  params_count += 1
        if R_body:   params_count += 1
        if R_topic:  params_count += 1
        #if S_clause: params_count += 1

        notes_count = len(st.session_state.hitl_notes)          # how many HITL notes

        m1, m2 = st.columns(2)

        m1.markdown(f'<div class="metric-card reveal"><div class="metric-num">{params_count}</div><div class="metric-lbl">Params Set</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card reveal"><div class="metric-num">{notes_count}</div><div class="metric-lbl">HITL Notes</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ----- Status badge -----

        badge = ('<span class="badge-ok">● Ready</span>'
                 if st.session_state.pdf_bytes
                 else '<span class="badge-wait">● Pending</span>')
        st.markdown(f"**Document Status:** {badge}", unsafe_allow_html=True)

        with st.expander("📖 Preview DRAFT Content", expanded=True):
            st.markdown(st.session_state.brd)

        st.divider()

        # use the stored bytes — do NOT regenerate on every rerun
        pdf_bytes = st.session_state.pdf_bytes

        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_bytes,
                file_name=f"DRAFT_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with col_b:
            if st.button("👁️ View PDF", use_container_width=True):
                st.session_state.show_pdf = not st.session_state.show_pdf

        # ----- Scrollable PDF viewer -----

        if st.session_state.show_pdf:
            b64 = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_display = f"""
                <iframe
                    class="pdf-frame"
                    src="data:application/pdf;base64,{b64}"
                    width="100%"
                    height="600px"
                    style="border:1px solid #ccc; border-radius:12px;
                           box-shadow:0 6px 18px rgba(0,0,0,0.15);">
                </iframe>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)

    else:
        st.info("👈 Set parameters on the left and click **Generate DRAFT**.")

   
