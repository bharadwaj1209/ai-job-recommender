import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

# Load correct GROQ API KEY (fix from your mistake)
GROQ_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_openai(prompt, max_tokens=500):
    """
    Sends a prompt to the Groq API and returns the response.
    Uses updated Llama 3.1 FREE model.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✔ WORKING MODEL (FREE)
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.5
    )

    return response.choices[0].message.content
