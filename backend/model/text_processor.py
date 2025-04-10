# backend/model/text_processor.py

import re
import string
from typing import List, Set, Dict

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')


class TextProcessor:
    """
    Class for text preprocessing and manipulation.
    """
    
    def __init__(self, language: str = "english"):
        """
        Initialize the text processor.
        
        Args:
            language (str): Language for stopwords and tokenization
        """
        self.language = language
        self.stop_words = set(stopwords.words(language))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess text by removing special characters, extra whitespace, etc.
        
        Args:
            text (str): Text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove special characters but keep periods, commas and other sentence punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)]', '', text)
        
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Replace multiple periods with single period
        text = re.sub(r'\.{2,}', '.', text)
        
        # Ensure proper spacing around punctuation
        text = re.sub(r'([\.,:;!?()])\s*', r'\1 ', text)
        
        return text.strip()
    
    def split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text (str): Text to split
            
        Returns:
            List[str]: List of sentences
        """
        return sent_tokenize(text)
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from a list of tokens.
        
        Args:
            tokens (List[str]): List of tokens
            
        Returns:
            List[str]: List of tokens with stopwords removed
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """
        Apply stemming to tokens.
        
        Args:
            tokens (List[str]): List of tokens
            
        Returns:
            List[str]: List of stemmed tokens
        """
        return [self.stemmer.stem(token) for token in tokens]
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Apply lemmatization to tokens.
        
        Args:
            tokens (List[str]): List of tokens
            
        Returns:
            List[str]: List of lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def get_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """
        Generate n-grams from tokens.
        
        Args:
            tokens (List[str]): List of tokens
            n (int): Size of n-grams
            
        Returns:
            List[str]: List of n-grams
        """
        return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    
    def tokenize_and_clean(self, text: str, remove_stops: bool = True, 
                           stem: bool = False, lemmatize: bool = False) -> List[str]:
        """
        Complete tokenization pipeline with cleaning options.
        
        Args:
            text (str): Input text
            remove_stops (bool): Whether to remove stopwords
            stem (bool): Whether to apply stemming
            lemmatize (bool): Whether to apply lemmatization
            
        Returns:
            List[str]: Processed tokens
        """
        # Preprocess text
        cleaned_text = self.preprocess(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Remove punctuation
        tokens = [token for token in tokens if token not in string.punctuation]
        
        # Remove stopwords if requested
        if remove_stops:
            tokens = self.remove_stopwords(tokens)
        
        # Apply stemming if requested
        if stem:
            tokens = self.stem_tokens(tokens)
        
        # Apply lemmatization if requested
        if lemmatize:
            tokens = self.lemmatize_tokens(tokens)
        
        return tokens