import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from typing import List, Optional

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class Summarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Split text into sentences and clean them."""
        sentences = sent_tokenize(text)
        return sentences
    
    def _sentence_similarity(self, sent1: str, sent2: str) -> float:
        """Calculate similarity between two sentences using cosine similarity."""
        words1 = [word.lower() for word in word_tokenize(sent1) if word.isalnum() and word.lower() not in self.stop_words]
        words2 = [word.lower() for word in word_tokenize(sent2) if word.isalnum() and word.lower() not in self.stop_words]
        
        # Create word vectors
        all_words = list(set(words1 + words2))
        vector1 = [1 if word in words1 else 0 for word in all_words]
        vector2 = [1 if word in words2 else 0 for word in all_words]
        
        # Calculate cosine similarity
        if len(all_words) == 0:
            return 0.0
        return 1 - cosine_distance(vector1, vector2)
    
    def _build_similarity_matrix(self, sentences: List[str]) -> np.ndarray:
        """Build similarity matrix for all sentences."""
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i == j:
                    continue
                similarity_matrix[i][j] = self._sentence_similarity(sentences[i], sentences[j])
                
        return similarity_matrix
    
    def summarize(self, text: str, length: str = "medium", output_format: str = "paragraph") -> str:
        """
        Generate a summary of the text.
        
        Args:
            text: Input text to summarize
            length: Length of summary (short, medium, large)
            output_format: Format of the output (paragraph, bullets, mindmap)
            
        Returns:
            Summarized text in the requested format
        """
        # Handle empty text
        if not text.strip():
            return "No text provided for summarization."
        
        # Preprocess text
        sentences = self._preprocess_text(text)
        
        # If text is very short, return the original
        if len(sentences) <= 3:
            return text
        
        # Build similarity matrix
        similarity_matrix = self._build_similarity_matrix(sentences)
        
        # Rank sentences using PageRank algorithm
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        
        # Sort sentences by score
        ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
        
        # Determine number of sentences to include based on length
        if length == "short":
            num_sentences = max(1, int(len(sentences) * 0.1))
        elif length == "medium":
            num_sentences = max(2, int(len(sentences) * 0.3))
        else:  # large
            num_sentences = max(3, int(len(sentences) * 0.5))
        
        num_sentences = min(num_sentences, len(sentences))
        
        # Get top sentences, but preserve original order
        selected_indices = [i for i, (score, _) in enumerate(ranked_sentences[:num_sentences])]
        selected_indices.sort()
        summary_sentences = [sentences[i] for i in selected_indices]
        
        # Format output
        if output_format == "paragraph":
            return " ".join(summary_sentences)
        elif output_format == "bullets":
            return "\n".join([f"• {sentence}" for sentence in summary_sentences])
        elif output_format == "mindmap":
            # For mindmap, we'll return a simple hierarchical structure
            # A more complex mindmap would require additional processing
            central_theme = summary_sentences[0] if summary_sentences else "Summary"
            branches = summary_sentences[1:] if len(summary_sentences) > 1 else ["No additional points"]
            
            mindmap = f"Central: {central_theme}\n"
            for i, branch in enumerate(branches, 1):
                mindmap += f"Branch {i}: {branch}\n"
            
            return mindmap
        else:
            return " ".join(summary_sentences)