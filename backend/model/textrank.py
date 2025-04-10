# backend/model/textrank.py

import numpy as np
import networkx as nx
from typing import List, Dict, Any

from .text_processor import TextProcessor


class TextRankSummarizer:
    """
    Implements the TextRank algorithm for extractive text summarization.
    TextRank is a graph-based ranking algorithm inspired by PageRank.
    """
    
    def __init__(self, damping: float = 0.85, max_iter: int = 100, 
                 convergence_threshold: float = 1e-5):
        """
        Initialize the TextRank summarizer.
        
        Args:
            damping (float): Damping factor for PageRank
            max_iter (int): Maximum number of iterations for PageRank
            convergence_threshold (float): Convergence threshold for PageRank
        """
        self.damping = damping
        self.max_iter = max_iter
        self.convergence_threshold = convergence_threshold
        self.text_processor = TextProcessor()
    
    def sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences.
        
        Args:
            sent1 (str): First sentence
            sent2 (str): Second sentence
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Tokenize and clean sentences
        tokens1 = self.text_processor.tokenize_and_clean(sent1, remove_stops=True)
        tokens2 = self.text_processor.tokenize_and_clean(sent2, remove_stops=True)
        
        # If either sentence has no tokens after cleaning, return 0
        if not tokens1 or not tokens2:
            return 0
        
        # Create sets of tokens
        set1 = set(tokens1)
        set2 = set(tokens2)
        
        # Calculate Jaccard similarity
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union) if union else 0
    
    def build_similarity_matrix(self, sentences: List[str]) -> np.ndarray:
        """
        Build a similarity matrix for all sentences.
        
        Args:
            sentences (List[str]): List of sentences
            
        Returns:
            np.ndarray: Similarity matrix
        """
        # Initialize similarity matrix
        n = len(sentences)
        similarity_matrix = np.zeros((n, n))
        
        # Compute similarity for each sentence pair
        for i in range(n):
            for j in range(n):
                if i != j:  # Skip self-similarity
                    similarity_matrix[i][j] = self.sentence_similarity(
                        sentences[i], sentences[j]
                    )
        
        return similarity_matrix
    
    def apply_pagerank(self, similarity_matrix: np.ndarray) -> Dict[int, float]:
        """
        Apply PageRank algorithm to the similarity matrix.
        
        Args:
            similarity_matrix (np.ndarray): Similarity matrix
            
        Returns:
            Dict[int, float]: Dictionary mapping sentence indices to their scores
        """
        # Create a graph from the similarity matrix
        graph = nx.from_numpy_array(similarity_matrix)
        
        # Apply PageRank
        scores = nx.pagerank(
            graph,
            alpha=self.damping,
            max_iter=self.max_iter,
            tol=self.convergence_threshold
        )
        
        return scores
    
    def summarize(self, sentences: List[str], num_sentences: int = 5) -> List[str]:
        """
        Generate a summary using TextRank.
        
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
        
        # Build similarity matrix
        similarity_matrix = self.build_similarity_matrix(sentences)
        
        # Apply PageRank to get sentence scores
        scores = self.apply_pagerank(similarity_matrix)
        
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
            'damping': self.damping,
            'max_iter': self.max_iter,
            'convergence_threshold': self.convergence_threshold
        }
    
    def set_params(self, params: Dict[str, Any]) -> None:
        """
        Set the parameters of the summarizer.
        
        Args:
            params (Dict[str, Any]): Dictionary of parameters
        """
        if 'damping' in params:
            self.damping = params['damping']
        if 'max_iter' in params:
            self.max_iter = params['max_iter']
        if 'convergence_threshold' in params:
            self.convergence_threshold = params['convergence_threshold']