# AI Job Recommender

An AI-powered job recommendation system that analyzes your resume and suggests relevant job listings, built with Streamlit and powered by LLMs (Groq / OpenAI).

## Features

- 📄 **Resume Upload & Parsing** — Upload a PDF resume; text is extracted automatically using PyMuPDF.
- 🤖 **AI-Powered Analysis** — Resume content is analyzed using Groq / OpenAI to understand skills, experience, and career profile.
- 💼 **Job Recommendations** — Fetches relevant job listings from LinkedIn and Naukri based on your profile.
- ⚡ **Simple Web Interface** — Built with Streamlit for a clean, interactive experience.

## Tech Stack

- **Frontend/App**: [Streamlit](https://streamlit.io/)
- **AI/LLM**: [Groq](https://groq.com/), [OpenAI](https://openai.com/)
- **PDF Parsing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- **Web Scraping**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- **Data Extraction**: [Apify Client](https://docs.apify.com/api/client/python/)
- **Environment Management**: python-dotenv

## Project Structure

```
ai-job-recommender/
├── app.py                 # Main Streamlit application
├── src/
│   ├── helper.py           # PDF text extraction & AI query functions
│   └── job_api.py          # Job fetching logic (LinkedIn, Naukri)
├── requirements.txt        # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- API keys for Groq and/or OpenAI
- Apify API token (if using Apify-based scraping)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bharadwaj1209/ai-job-recommender.git
   cd ai-job-recommender
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   APIFY_API_TOKEN=your_apify_token
   ```

### Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Deployment

This app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

> **Note**: If you're deploying and see a `ModuleNotFoundError`, make sure only **one** dependency file (`requirements.txt`) exists in the repo. Having `uv.lock` or `pyproject.toml` alongside it can cause Streamlit Cloud to skip `requirements.txt` entirely.

## How It Works

1. User uploads their resume (PDF).
2. `extract_text_from_pdf()` extracts raw text using PyMuPDF.
3. `ask_openai()` (via Groq/OpenAI) analyzes the resume content — skills, experience, role fit.
4. `fetch_linkedin_jobs()` and `fetch_naukri_jobs()` pull matching job listings based on the analysis.
5. Results are displayed in the Streamlit UI.

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key for Groq LLM access |
| `OPENAI_API_KEY` | API key for OpenAI access |
| `APIFY_API_TOKEN` | API token for Apify-based job scraping |

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Chandra Prakash (Banty)**
B.Tech Information Technology, BNCET Lucknow