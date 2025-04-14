# 📄 Document Summarization Tool using NLP

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-green.svg)

A powerful text summarization application that uses traditional Natural Language Processing techniques to create concise, high-quality summaries of documents. This tool employs extractive summarization algorithms without relying on Large Language Models, making it lightweight and efficient for various document types.


## ✨ Features

- **Multiple Summarization Methods**: TextRank (graph-based), TF-IDF (frequency-based), and Ensemble approaches
- **File Support**: Process text files, PDFs, Word documents, HTML, and Markdown
- **RESTful API**: Easily integrate summarization into your own applications
- **Customizable**: Adjust summary length, language, and summarization method
- **Performance Metrics**: View compression ratios and processing times

## 🛠️ Prerequisites

- Python 3.8 or higher
- Node.js and npm (for Tailwind CSS compilation)

## 🚀 Deployment

Follow these steps to deploy the project on your local system:

### 1. Clone the Repository

```bash
git clone https://github.com/aka-harsh/document-summarizer.git
cd document-summarizer
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Download required NLTK resources
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### 3. Install PDF Processing Libraries

```bash
pip install PyPDF2 pdfplumber python-docx html2text
```

### 4. Start the Backend Server

```bash
# From the project root directory:
python backend/main.py --api --port 8000
```

You should see output indicating the server is running at http://localhost:8000.

### 5. Open the Frontend

Simply open the `frontend/index.html` file in your web browser:

```bash
# For macOS:
open frontend/index.html
# For Linux:
xdg-open frontend/index.html
# For Windows:
start frontend/index.html
```

Alternatively, you can drag and drop the HTML file into your browser window.

### 6. Using the Application

1. Enter text or upload a document (TXT, PDF, DOCX, HTML, MD)
2. Select your preferred summarization method:
   - **TextRank**: Graph-based algorithm, good for structured texts
   - **TF-IDF**: Frequency-based approach, emphasizes key terms
   - **Ensemble**: Combines both methods for balanced results
3. Adjust the summary length slider to get shorter or longer summaries
4. Click "Generate Summary" to process your document
5. View your summary and performance metrics

### 7. API Usage

The application provides a RESTful API for integration with other systems:

```bash
# Example API request using curl:
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text to summarize...", "model_type": "ensemble", "ratio": 0.3, "language": "english"}'
```

## 🔭 Project Outlook
