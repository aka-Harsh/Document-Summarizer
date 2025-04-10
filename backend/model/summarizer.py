# backend/model/summarizer.py

import os
import pickle
import numpy as np
from typing import List, Dict, Tuple, Union, Optional

from .text_processor import TextProcessor
from .textrank import TextRankSummarizer
from .tfidf_summarizer import TFIDFSummarizer


class DocumentSummarizer:
    """
    Main document summarization class that integrates different summarization techniques.
    """
    
    def __init__(self, model_type: str = "textrank", language: str = "english"):
        """
        Initialize the document summarizer.
        
        Args:
            model_type (str): Type of summarization model to use ('textrank', 'tfidf', or 'ensemble')
            language (str): Language of the documents to summarize
        """
        self.model_type = model_type
        self.language = language
        self.text_processor = TextProcessor(language=language)
        
        # Initialize summarizers
        self.textrank_summarizer = TextRankSummarizer()
        self.tfidf_summarizer = TFIDFSummarizer()
        
        # Model weights for ensemble approach
        self.model_weights = {
            'textrank': 0.6,
            'tfidf': 0.4
        }
    
    def summarize(self, text: str, ratio: float = 0.3, min_length: int = 100, 
                 max_length: int = 500) -> Dict[str, Union[str, float]]:
        """
        Generate a summary of the input text.
        
        Args:
            text (str): The text to summarize
            ratio (float): The target ratio of summary to original text length
            min_length (int): Minimum length of summary in characters
            max_length (int): Maximum length of summary in characters
            
        Returns:
            Dict: Summary results including the summary text, statistics, and metadata
        """
        # Preprocess the text
        cleaned_text = self.text_processor.preprocess(text)
        sentences = self.text_processor.split_sentences(cleaned_text)
        
        # Calculate target summary length
        target_sentences = max(1, int(len(sentences) * ratio))
        
        # Generate summary based on selected model
        if self.model_type == "textrank":
            summary_sentences = self.textrank_summarizer.summarize(
                sentences, target_sentences
            )
        elif self.model_type == "tfidf":
            summary_sentences = self.tfidf_summarizer.summarize(
                sentences, target_sentences
            )
        elif self.model_type == "ensemble":
            # Get both summaries
            tr_sentences = self.textrank_summarizer.summarize(
                sentences, target_sentences
            )
            tfidf_sentences = self.tfidf_summarizer.summarize(
                sentences, target_sentences
            )
            
            # Combine results using weighted approach
            summary_scores = {}
            for sentence in set(tr_sentences + tfidf_sentences):
                score = 0
                if sentence in tr_sentences:
                    idx = tr_sentences.index(sentence)
                    score += self.model_weights['textrank'] * (1 - idx/len(tr_sentences))
                if sentence in tfidf_sentences:
                    idx = tfidf_sentences.index(sentence)
                    score += self.model_weights['tfidf'] * (1 - idx/len(tfidf_sentences))
                summary_scores[sentence] = score
            
            # Select top sentences by score
            sorted_sentences = sorted(
                summary_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            selected_sentences = [s[0] for s in sorted_sentences[:target_sentences]]
            
            # Reorder sentences to match original text flow
            summary_sentences = [s for s in sentences if s in selected_sentences]
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Create the final summary
        summary_text = " ".join(summary_sentences)
        
        # Compile statistics
        original_word_count = len(text.split())
        summary_word_count = len(summary_text.split())
        compression_ratio = summary_word_count / original_word_count if original_word_count > 0 else 0
        
        return {
            "summary": summary_text,
            "original_length": original_word_count,
            "summary_length": summary_word_count,
            "compression_ratio": compression_ratio,
            "model_used": self.model_type,
            "sentence_count": len(summary_sentences)
        }
    
    def save_model(self, path: str) -> None:
        """
        Save the current model configuration to disk.
        
        Args:
            path (str): Path to save the model
        """
        model_data = {
            'model_type': self.model_type,
            'language': self.language,
            'model_weights': self.model_weights,
            'textrank_params': self.textrank_summarizer.get_params(),
            'tfidf_params': self.tfidf_summarizer.get_params()
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save model to disk
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, path: str) -> None:
        """
        Load a saved model configuration.
        
        Args:
            path (str): Path to the saved model
        """
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model_type = model_data['model_type']
        self.language = model_data['language']
        self.model_weights = model_data['model_weights']
        
        # Re-initialize text processor with loaded language
        self.text_processor = TextProcessor(language=self.language)
        
        # Update model parameters
        self.textrank_summarizer.set_params(model_data['textrank_params'])
        self.tfidf_summarizer.set_params(model_data['tfidf_params'])
    
    def train(self, documents: List[str], summaries: List[str]) -> Dict:
        """
        Train the model weights based on provided document-summary pairs.
        
        Args:
            documents (List[str]): List of original documents
            summaries (List[str]): List of ground truth summaries
            
        Returns:
            Dict: Training results including accuracy metrics
        """
        # This is a simplified training approach to adjust model weights
        # In a real implementation, you would use more sophisticated techniques
        
        best_weights = {'textrank': 0.5, 'tfidf': 0.5}
        best_score = 0
        
        # Try different weight combinations
        for tr_weight in np.arange(0.1, 1.0, 0.1):
            tfidf_weight = 1 - tr_weight
            self.model_weights = {'textrank': tr_weight, 'tfidf': tfidf_weight}
            
            total_score = 0
            for doc, ref_summary in zip(documents, summaries):
                # Generate summary with current weights
                self.model_type = "ensemble"
                result = self.summarize(doc)
                summary = result['summary']
                
                # Calculate simple similarity score (could use ROUGE or other metrics)
                score = self._calc_simple_similarity(summary, ref_summary)
                total_score += score
            
            avg_score = total_score / len(documents) if documents else 0
            
            if avg_score > best_score:
                best_score = avg_score
                best_weights = self.model_weights.copy()
        
        # Set the best weights
        self.model_weights = best_weights
        
        return {
            'best_weights': best_weights,
            'best_score': best_score
        }
    
    def _calc_simple_similarity(self, summary: str, reference: str) -> float:
        """
        Calculate a simple similarity score between generated and reference summaries.
        
        Args:
            summary (str): Generated summary
            reference (str): Reference (ground truth) summary
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Convert to sets of words for simple overlap calculation
        summary_words = set(self.text_processor.tokenize(summary.lower()))
        reference_words = set(self.text_processor.tokenize(reference.lower()))
        
        # Calculate Jaccard similarity
        if not summary_words or not reference_words:
            return 0
        
        intersection = len(summary_words.intersection(reference_words))
        union = len(summary_words.union(reference_words))
        
        return intersection / union if union > 0 else 0