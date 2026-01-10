# Document Summarization Tool using NLP

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-green.svg)

A powerful text summarization application that uses traditional Natural Language Processing techniques to create concise, high-quality summaries of documents. This tool employs extractive summarization algorithms without relying on Large Language Models, making it lightweight and efficient for various document types.

## Prerequisites

- Python 3.8 or higher
- Node.js and npm

## Deployment

Follow these steps to run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/aka-harsh/document-summarizer.git
cd document-summarizer
```

### 2. Set Up Python Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# NLTK resources
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```


### 3. Start Backend Server

```bash
# From the project root directory:
python backend/main.py --api --port 8000
```


### 4. Start Frontend

Simply open the `frontend/index.html` file in your web browser:

```bash
# For macOS:
open frontend/index.html
# For Linux:
xdg-open frontend/index.html
# For Windows:
start frontend/index.html
```

### 5. API Usage

The application provides a RESTful API for integration with other systems:

```bash
# Example API request using curl:
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text to summarize...", "model_type": "ensemble", "ratio": 0.3, "language": "english"}'
```

## 🔭 Project Outlook <br>

![Image](https://github.com/user-attachments/assets/b52bae9a-5fef-4169-b4cc-576d265c8b7c)
![Image](https://github.com/user-attachments/assets/298c289b-1d05-4023-8ddb-91755a79c941)
![Image](https://github.com/user-attachments/assets/b919cd3d-61f9-40e3-8cfd-c76b250e4a6a)
![Image](https://github.com/user-attachments/assets/1942e804-e1a3-4336-883e-11cecd932d86)
