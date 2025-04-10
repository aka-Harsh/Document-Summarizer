# backend/model/tfidf_summarizer.py

import numpy as np
from typing import List, Dict, Any
from collections import Counter
import math

from .text_processor import TextProcessor


class TFIDFSummarizer:
    """
    Implements TF-IDF based extractive text summarization.
    """
    
    def __init__(self, use_idf: bool = True, smooth_idf: bool = True, 
                 sublinear_tf: bool = False, min_df: int = 1):
        """
        Initialize the TF-IDF summarizer.
        
        Args:
            use_idf (bool): Whether to use inverse document frequency
            smooth_idf (bool): Whether to smooth IDF weights
            sublinear_tf (bool): Whether to use sublinear term frequency scaling
            min_df (int): Minimum document frequency for a term to be included
        """
        self.use_idf = use_idf
        self.smooth_idf = smooth_idf
        self.sublinear_tf = sublinear_tf
        self.min_df = min_df
        self.text_processor = TextProcessor()
    
    def compute_tf(self, sentence: str) -> Dict[str, float]:
        """
        Compute term frequency for a sentence.
        
        Args:
            sentence (str): Input sentence
            
        Returns:
            Dict[str, float]: Term frequency dictionary
        """
        # Tokenize and clean the sentence
        tokens = self.text_processor.tokenize_and_clean(sentence, remove_stops=True)
        
        # Count the terms
        term_counts = Counter(tokens)
        total_terms = len(tokens) if tokens else 1
        
        # Compute term frequency
        tf = {}
        for term, count in term_counts.items():
            if self.sublinear_tf:
                # Apply sublinear scaling (1 + log(tf))
                tf[term] = 1 + math.log(count) if count > 0 else 0
            else:
                # Regular term frequency (count / total)
                tf[term] = count / total_terms
        
        return tf
    
    def compute_idf(self, sentences: List[str]) -> Dict[str, float]:
        """
        Compute inverse document frequency for all terms in the sentences.
        
        Args:
            sentences (List[str]): List of sentences
            
        Returns:
            Dict[str, float]: Inverse document frequency dictionary
        """
        # Count document frequency for each term
        df = Counter()
        for sentence in sentences:
            # Get unique terms in the sentence
            tokens = set(self.text_processor.tokenize_and_clean(sentence, remove_stops=True))
            df.update(tokens)
        
        # Total number of documents (sentences)
        n_docs = len(sentences)
        
        # Compute IDF
        idf = {}
        for term, doc_freq in df.items():
            # Skip terms with document frequency below min_df
            if doc_freq < self.min_df:
                continue
            
            if self.smooth_idf:
                # Smooth IDF: log((1+n)/(1+df)) + 1
                idf[term] = math.log((1 + n_docs) / (1 + doc_freq)) + 1
            else:
                # Regular IDF: log(n/df)
                idf[term] = math.log(n_docs / doc_freq) if doc_freq > 0 else 0
        
        return idf
    
    def compute_tfidf_scores(self, sentences: List[str]) -> Dict[int, float]:
        """
        Compute TF-IDF scores for all sentences.
        
        Args:
            sentences (List[str]): List of sentences
            
        Returns:
            Dict[int, float]: Dictionary mapping sentence indices to their scores
        """
        # Compute IDF if using it
        idf = self.compute_idf(sentences) if self.use_idf else {}
        
        # Compute TF-IDF score for each sentence
        scores = {}
        for i, sentence in enumerate(sentences):
            # Compute TF for the sentence
            tf = self.compute_tf(sentence)
            
            # Compute TF-IDF score
            if self.use_idf:
                score = sum(tf.get(term, 0) * idf.get(term, 0) for term in tf)
            else:
                score = sum(tf.values())
            
            # Normalize by sentence length to avoid favoring long sentences
            token_count = len(self.text_processor.tokenize_and_clean(sentence))
            if token_count > 0:
                score /= token_count
            
            scores[i] = score
        
        return scores
    
    def summarize(self, sentences: List[str], num_sentences: int = 5) -> List[str]:
        """
        Generate a summary using TF-IDF.
        
        Args:
            sentences (List[str]): List of sentences
            num_sentences (int): Number of sentences in the summary
            
        Returns:
            List[str]: Summary sentences
        """
        # Handle edge cases
        if not sentences:
            return []
        
        if len(sentences) <= num_sentences:
            return sentences
        
        # Compute TF-IDF scores
        scores = self.compute_tfidf_scores(sentences)
        
        # Rank sentences by score
        ranked_sentences = sorted(
            ((scores[i], s, i) for i, s in enumerate(sentences)),
            reverse=True
        )
        
        # Select top sentences
        top_sentences = ranked_sentences[:num_sentences]
        
        # Sort selected sentences by their original position
        top_sentences.sort(key=lambda x: x[2])
        
        # Return the sentences
        return [s[1] for s in top_sentences]
    
    def get_params(self) -> Dict[str, Any]:
        """
        Get the current parameters of the summarizer.
        
        Returns:
            Dict[str, Any]: Dictionary of parameters
        """
        return {
            'use_idf': self.use_idf,
            'smooth_idf': self.smooth_idf,
            'sublinear_tf': self.sublinear_tf,
            'min_df': self.min_df
        }
    
    def set_params(self, params: Dict[str, Any]) -> None:
        """
        Set the parameters of the summarizer.
        
        Args:
            params (Dict[str, Any]): Dictionary of parameters
        """
        if 'use_idf' in params:
            self.use_idf = params['use_idf']
        if 'smooth_idf' in params:
            self.smooth_idf = params['smooth_idf']
        if 'sublinear_tf' in params:
            self.sublinear_tf = params['sublinear_tf']
        if 'min_df' in params:
            self.min_df = params['min_df']