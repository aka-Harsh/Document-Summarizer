# backend/model/evaluator.py

from typing import List, Dict, Any, Union
import numpy as np
from collections import Counter

class SummaryEvaluator:
    """
    Evaluates the quality of generated summaries.
    """
    
    def __init__(self):
        pass
    
    def rouge_n(self, reference: str, summary: str, n: int = 1) -> float:
        """
        Calculate ROUGE-N score (recall-oriented metric).
        
        Args:
            reference (str): Reference (ground truth) summary
            summary (str): Generated summary
            n (int): N-gram size
            
        Returns:
            float: ROUGE-N score
        """
        # Get n-grams from reference and summary
        ref_ngrams = self._get_ngrams(reference.lower().split(), n)
        sum_ngrams = self._get_ngrams(summary.lower().split(), n)
        
        # Count matching n-grams
        matches = sum(min(ref_ngrams.get(ngram, 0), sum_ngrams.get(ngram, 0)) 
                      for ngram in sum_ngrams)
        
        # Calculate ROUGE-N (recall)
        if sum(ref_ngrams.values()) == 0:
            return 0.0
        
        return matches / sum(ref_ngrams.values())
    
    def _get_ngrams(self, tokens: List[str], n: int) -> Dict[str, int]:
        """
        Get n-grams with their frequencies from tokens.
        
        Args:
            tokens (List[str]): List of tokens
            n (int): N-gram size
            
        Returns:
            Dict[str, int]: Dictionary mapping n-grams to their frequencies
        """
        ngrams = Counter()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams[ngram] += 1
        
        return ngrams
    
    def evaluate_summary(self, reference: str, summary: str) -> Dict[str, float]:
        """
        Evaluate a summary using multiple metrics.
        
        Args:
            reference (str): Reference (ground truth) summary
            summary (str): Generated summary
            
        Returns:
            Dict[str, float]: Dictionary of evaluation metrics
        """
        # Calculate ROUGE scores
        rouge_1 = self.rouge_n(reference, summary, 1)
        rouge_2 = self.rouge_n(reference, summary, 2)
        
        return {
            'rouge_1': rouge_1,
            'rouge_2': rouge_2,
            'average_rouge': (rouge_1 + rouge_2) / 2
        }