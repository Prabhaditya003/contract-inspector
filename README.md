# AI Consumer Contract & Rental Lease Inspector

A Streamlit-based web application that utilizes NLP to parse residential lease agreements, employment contracts, and service terms. The tool scans documents for predatory clauses, illegal security deposit deductions, unilateral liability waivers, and hidden fees, outputting plain-language explanations for general consumers.

## Features
* **PDF Parsing:** Extracts raw text from uploaded contract documents.
* **Automated NLP Analysis:** Identifies high-risk clauses and missing standard protections.
* **Minimalist UI:** Clean, distraction-free black-and-white dashboard.

## Tech Stack
* **Frontend/Backend:** Python, Streamlit
* **PDF Processing:** PyPDF2
* **LLM Integration:** Google Gemini 1.5 Flash via `google-generativeai`

## Local Installation
1. Clone the repository: `git clone https://github.com/YOUR_USERNAME/contract-inspector.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.streamlit/secrets.toml` file in the root directory and add your API key:
   `GEMINI_API_KEY = "your_api_key_here"`
4. Run the application: `streamlit run app.py`