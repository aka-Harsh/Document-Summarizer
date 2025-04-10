from setuptools import setup, find_packages

setup(
    name="document-summarizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "numpy",
        "networkx",
        "scikit-learn",
        "fastapi",
        "uvicorn",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Document summarization tool",
)