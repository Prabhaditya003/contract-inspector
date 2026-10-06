import html
import streamlit as st
from google import genai
import PyPDF2

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Contract Inspector",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# STYLES — monochrome palette, Inter font
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --ink: #080808;
        --paper: #ffffff;
        --canvas: #f3f3f3;
        --muted: #686868;
        --line: #e2e2e2;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--ink);
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: var(--canvas) !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 1180px !important;
        padding: 0 34px 56px !important;
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-height: 76px;
        border-bottom: 1px solid #dedede;
        margin-bottom: 58px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        color: #080808;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: -0.03em;
    }

    .brand-mark {
        display: grid;
        place-items: center;
        width: 32px;
        height: 32px;
        border-radius: 9px;
        background: #080808;
        color: #fff;
        font-size: 11px;
        font-weight: 600;
    }

    .topbar-note {
        color: #686868;
        font-size: 12px;
    }

    .eyebrow {
        display: flex;
        align-items: center;
        gap: 9px;
        margin-bottom: 19px;
        color: #666;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: .12em;
        text-transform: uppercase;
    }

    .eyebrow-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #080808;
    }

    .hero-title {
        margin: 0 0 22px;
        color: #080808;
        font-size: clamp(48px, 6.3vw, 76px);
        font-weight: 500;
        letter-spacing: -.067em;
        line-height: .98;
    }

    .hero-copy {
        max-width: 690px;
        color: #555;
        font-size: 16px;
        line-height: 1.75;
    }

    .hero-side {
        margin-top: 22px;
        padding-left: 24px;
        border-left: 1px solid #dedede;
    }

    .feature {
        padding: 14px 0;
        border-bottom: 1px solid #e2e2e2;
    }

    .feature:last-child { border-bottom: 0; }

    .feature-title {
        color: #080808;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .feature-copy {
        color: #707070;
        font-size: 12px;
        line-height: 1.5;
    }

    .section-card {
        margin-top: 48px;
        overflow: hidden;
        border: 1px solid #dedede;
        border-radius: 18px;
        background: #fff;
        box-shadow: 0 14px 42px rgba(0,0,0,.045);
    }

    .section-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 23px 27px;
        border-bottom: 1px solid #e7e7e7;
    }

    .section-title {
        color: #080808;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: -.02em;
    }

    .section-step {
        color: #777;
        font-size: 10px;
        letter-spacing: .08em;
    }

    .upload-inner {
        padding: 28px;
    }

    .field-label {
        margin-bottom: 13px;
        color: #666;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: .1em;
        text-transform: uppercase;
    }

    [data-testid="stFileUploader"] {
        width: 100%;
    }

    [data-testid="stFileUploadDropzone"] {
        min-height: 180px;
        border: 1px dashed #bdbdbd !important;
        border-radius: 13px !important;
        background: #fafafa !important;
        transition: border-color .2s ease, background .2s ease;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #080808 !important;
        background: #f6f6f6 !important;
    }

    [data-testid="stFileUploadDropzone"] * {
        color: #080808 !important;
    }

    [data-testid="stFileUploadDropzone"] small {
        color: #777 !important;
    }

    .file-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-top: 16px;
        padding: 15px 17px;
        border: 1px solid #e1e1e1;
        border-radius: 12px;
        background: #fafafa;
    }

    .file-left {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }

    .file-icon {
        display: grid;
        place-items: center;
        flex-shrink: 0;
        width: 38px;
        height: 38px;
        border-radius: 9px;
        background: #080808;
        color: #fff;
        font-size: 10px;
        font-weight: 600;
    }

    .file-name {
        overflow-wrap: anywhere;
        color: #080808;
        font-size: 12px;
        font-weight: 600;
    }

    .file-meta {
        margin-top: 4px;
        color: #777;
        font-size: 11px;
    }

    .ready-pill {
        flex-shrink: 0;
        padding: 6px 10px;
        border-radius: 20px;
        background: #eeeeee;
        color: #111;
        font-size: 10px;
        font-weight: 600;
    }

    .stButton > button {
        width: 100%;
        min-height: 54px;
        margin-top: 18px;
        border: 1px solid #080808;
        border-radius: 11px;
        background: #080808;
        color: #fff;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 500;
        transition: background .2s ease, transform .2s ease;
    }

    .stButton > button:hover {
        border-color: #292929;
        background: #292929;
        color: #fff;
        transform: translateY(-1px);
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 2px #fff, 0 0 0 4px #080808;
    }

    .steps {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        border-top: 1px solid #e7e7e7;
    }

    .step-item {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 20px 24px;
        color: #555;
        font-size: 11px;
    }

    .step-number {
        display: grid;
        place-items: center;
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        border-radius: 50%;
        background: #f0f0f0;
        color: #111;
        font-size: 10px;
        font-weight: 600;
    }

    .step-number.active {
        background: #080808;
        color: #fff;
    }

    .results-heading {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 12px;
        margin: 54px 0 18px;
    }

    .results-title {
        color: #080808;
        font-size: 31px;
        font-weight: 500;
        letter-spacing: -.05em;
    }

    .results-status {
        color: #777;
        font-size: 10px;
        letter-spacing: .08em;
    }

    .result-panel {
        padding: 28px;
        border: 1px solid #dedede;
        border-radius: 17px;
        background: #fff;
        box-shadow: 0 12px 35px rgba(0,0,0,.04);
    }

    .result-panel h1, .result-panel h2, .result-panel h3 {
        color: #080808 !important;
        letter-spacing: -.035em;
    }

    .result-panel h2 { font-size: 21px; }
    .result-panel h3 { font-size: 16px; }

    .result-panel p, .result-panel li {
        color: #444 !important;
        font-size: 13px;
        line-height: 1.8;
    }

    .result-panel strong { color: #080808 !important; }

    .disclaimer {
        margin-top: 14px;
        padding: 15px 17px;
        border: 1px solid #dedede;
        border-radius: 11px;
        background: #fafafa;
        color: #686868;
        font-size: 11px;
        line-height: 1.65;
    }

    .footer {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        margin-top: 54px;
        padding-top: 20px;
        border-top: 1px solid #dedede;
        color: #888;
        font-size: 10px;
        letter-spacing: .04em;
    }

    @media (max-width: 760px) {
        .block-container { padding: 0 17px 38px !important; }
        .topbar { margin-bottom: 40px; }
        .topbar-note { font-size: 10px; }
        .hero-title { font-size: 52px; }
        .hero-copy { font-size: 14px; }
        .hero-side { margin-top: 28px; }
        .section-card { margin-top: 34px; }
        .section-head { padding: 19px; }
        .upload-inner { padding: 19px; }
        .steps { grid-template-columns: 1fr; }
        .step-item { padding: 13px 19px; }
        .result-panel { padding: 20px; }
        .footer { flex-direction: column; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# API CONFIGURATION
# ------------------------------------------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error(
        "Gemini API key not found. Add GEMINI_API_KEY to "
        ".streamlit/secrets.toml before running the app."
    )
    st.stop()

# Replaced genai.configure() with the modern genai.Client() initialization
client = genai.Client(api_key=GEMINI_API_KEY)


def extract_text_from_pdf(file):
    """Extract selectable text from each page of an uploaded PDF."""
    reader = PyPDF2.PdfReader(file)
    pages = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)

    return "\n\n".join(pages)


def analyze_contract(contract_text):
    """Ask Gemini to identify clauses that deserve closer review."""
    prompt = f"""
You are an AI assistant that helps people review contracts in plain language.
This is informational assistance, not a legal determination.

Review the contract text and flag clauses that may deserve further review:
1. Potentially predatory or unusually one-sided clauses
2. Security deposit deductions or forfeiture terms
3. Unilateral liability waivers or broad releases
4. Hidden fees, penalties, automatic renewals, or unclear charges

For each finding:
- Give a short descriptive heading.
- Quote or identify the relevant wording when possible.
- Explain the possible concern in plain language.
- Suggest a practical question the user could ask the other party.

Do not claim a clause is illegal unless the contract text and applicable jurisdiction
provide enough information. Explain that legality depends on location and circumstances.
If you find no obvious red flags, say so cautiously and list 2-3 clauses worth reviewing.
Use clear Markdown headings and bullet points.

CONTRACT TEXT:
{contract_text}
"""
    # Updated to the new SDK syntax and gemini-2.5-flash model
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )
    return response.text or "The model returned an empty response. Please try again."


# ------------------------------------------------------------
# TOP BAR
# ------------------------------------------------------------
st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <div class="brand-mark">CI</div>
            <span>Contract Inspector</span>
        </div>
        <div class="topbar-note">AI-powered contract review</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
hero_left, hero_right = st.columns([1.8, 1], gap="large")

with hero_left:
    st.markdown(
        """
        <div class="eyebrow">
            <span class="eyebrow-dot"></span>
            Legal document intelligence
        </div>
        <div class="hero-title">Understand<br>what you sign.</div>
        <div class="hero-copy">
            Upload a residential lease or service agreement. Contract Inspector
            helps surface potentially one-sided clauses, hidden fees, and unusual
            liability terms so you know what to review before signing.
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
        <div class="hero-side">
            <div class="feature">
                <div class="feature-title">01 &nbsp; Spot risky clauses</div>
                <div class="feature-copy">Find terms that may deserve a closer look.</div>
            </div>
            <div class="feature">
                <div class="feature-title">02 &nbsp; Understand your rights</div>
                <div class="feature-copy">Get plain-language explanations of contract wording.</div>
            </div>
            <div class="feature">
                <div class="feature-title">03 &nbsp; Make informed decisions</div>
                <div class="feature-copy">Know what questions to ask before you sign.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# UPLOAD WORKSPACE
# ------------------------------------------------------------
st.markdown(
    """
    <div class="section-card">
        <div class="section-head">
            <div class="section-title">Document analysis</div>
            <div class="section-step">STEP 01 / UPLOAD</div>
        </div>
        <div class="upload-inner">
            <div class="field-label">Contract document · PDF only</div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Drop your PDF here or browse your files",
    type=["pdf"],
    help="Upload a PDF containing selectable text. Scanned image-only PDFs may not work.",
)

if uploaded_file is not None:
    safe_name = html.escape(uploaded_file.name)
    size_kb = uploaded_file.size / 1024

    st.markdown(
        f"""
        <div class="file-card">
            <div class="file-left">
                <div class="file-icon">PDF</div>
                <div>
                    <div class="file-name">{safe_name}</div>
                    <div class="file-meta">{size_kb:.1f} KB · PDF document</div>
                </div>
            </div>
            <div class="ready-pill">READY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

analyze_clicked = st.button(
    "Analyze contract  →",
    type="primary",
    disabled=uploaded_file is None,
)

st.markdown(
    """
        </div>
        <div class="steps">
            <div class="step-item">
                <span class="step-number active">01</span>
                <span>Upload document</span>
            </div>
            <div class="step-item">
                <span class="step-number">02</span>
                <span>AI reviews clauses</span>
            </div>
            <div class="step-item">
                <span class="step-number">03</span>
                <span>Review potential risks</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# ANALYZE DOCUMENT
# ------------------------------------------------------------
if analyze_clicked and uploaded_file is not None:
    try:
        with st.spinner("Reading your document and reviewing its clauses..."):
            contract_text = extract_text_from_pdf(uploaded_file)

            if not contract_text.strip():
                st.error(
                    "No selectable text was found in this PDF. It may be a scanned "
                    "document; OCR would be needed before analysis."
                )
            else:
                result = analyze_contract(contract_text)
                st.session_state["contract_analysis"] = result
                st.session_state["contract_filename"] = uploaded_file.name
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")

# ------------------------------------------------------------
# RESULTS — persists across Streamlit reruns
# ------------------------------------------------------------
if st.session_state.get("contract_analysis"):
    result_name = html.escape(st.session_state.get("contract_filename", "Uploaded PDF"))

    st.markdown(
        f"""
        <div class="results-heading">
            <div class="results-title">Analysis</div>
            <div class="results-status">REVIEW COMPLETE · {result_name}</div>
        </div>
        <div class="result-panel">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(st.session_state["contract_analysis"])

    st.markdown(
        """
        </div>
        <div class="disclaimer">
            <strong>Important:</strong> This AI-generated review is for informational
            purposes only and is not legal advice. Whether a clause is enforceable
            depends on the applicable law and circumstances. Consider consulting a
            qualified legal professional before making decisions about a contract.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <span>CONTRACT INSPECTOR</span>
        <span>AI-ASSISTED REVIEW · NOT LEGAL ADVICE</span>
    </div>
    """,
    unsafe_allow_html=True,
)