# LegalEase

LegalEase is an AI-powered legal document drafting application built using:

- Python
- FastAPI
- Streamlit
- Google Gemini
- python-docx
- FPDF

## Features

- AI legal document generation
- Employment contracts
- NDA
- Lease agreements
- Service agreements
- Freelance agreements
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Logo support
- FastAPI backend
- Streamlit frontend

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file from the sample and add your Gemini API key:

```bash
copy .env.example .env
```

Start each service in a separate terminal from the project directory:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

```bash
streamlit run frontend/app.py --server.port 8501
```