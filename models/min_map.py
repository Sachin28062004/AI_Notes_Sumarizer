import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from collections import Counter
import networkx as nx
from typing import Dict, List, Tuple, Any

# Download necessary NLTK data
nltk.download('averaged_perceptron_tagger', quiet=True)

class MindMapGenerator:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
    def extract_key_concepts(self, text: str, max_concepts: int = 7) -> List[str]:
        """Extract key concepts from text."""
        # Tokenize and filter words
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        # Get word frequency
        word_freq = Counter(filtered_words)
        
        # Get part-of-speech tags
        pos_tags = pos_tag(list(word_freq.keys()))
        
        # Extract nouns which are likely to be concepts
        nouns = [(word, word_freq[word]) for word, tag in pos_tags if tag.startswith('NN')]
        
        # Sort by frequency and take top N
        top_concepts = [word for word, _ in sorted(nouns, key=lambda x: x[1], reverse=True)[:max_concepts]]
        
        return top_concepts
        
    def extract_relationships(self, text: str, concepts: List[str]) -> Dict[str, List[str]]:
        """Extract relationships between concepts."""
        sentences = sent_tokenize(text)
        relationships = {concept: [] for concept in concepts}
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Check which concepts appear in this sentence
            present_concepts = [concept for concept in concepts if concept in sentence_lower]
            
            # If multiple concepts appear in the same sentence, they might be related
            if len(present_concepts) > 1:
                for i, concept1 in enumerate(present_concepts):
                    for concept2 in present_concepts[i+1:]:
                        if concept2 not in relationships[concept1]:
                            relationships[concept1].append(concept2)
                        if concept1 not in relationships[concept2]:
                            relationships[concept2].append(concept1)
        
        return relationships
    
    def generate_mindmap(self, text: str, format_type: str = "text") -> str:
        """Generate a mind map from text."""
        # Extract concepts
        concepts = self.extract_key_concepts(text)
        if not concepts:
            return "Could not generate mind map: no key concepts found."
        
        # Extract relationships
        relationships = self.extract_relationships(text, concepts)
        
        # Select main concept (most connected)
        main_concept = max(concepts, key=lambda c: len(relationships[c]))
        
        # Generate mind map based on format type
        if format_type == "text":
            # Simple text-based mind map
            mindmap = f"Central Topic: {main_concept.capitalize()}\n"
            
            # Add branches
            for i, concept in enumerate(concepts):
                if concept != main_concept:
                    mindmap += f"Branch {i}: {concept.capitalize()}\n"
                    
                    # Add sub-branches (related concepts)
                    for j, related in enumerate(relationships[concept]):
                        if related != main_concept and related in concepts:
                            mindmap += f"  Sub-branch {i}.{j}: {related.capitalize()}\n"
            
            return mindmap
            
        elif format_type == "json":
            # JSON structure for use with visualization libraries
            mindmap_data = {
                "central": main_concept.capitalize(),
                "branches": []
            }
            
            for concept in concepts:
                if concept != main_concept:
                    branch = {
                        "name": concept.capitalize(),
                        "sub_branches": []
                    }
                    
                    for related in relationships[concept]:
                        if related != main_concept and related in concepts:
                            branch["sub_branches"].append({
                                "name": related.capitalize()
                            })
                    
                    mindmap_data["branches"].append(branch)
            
            import json
            return json.dumps(mindmap_data, indent=2)
            
        else:
            return "Unsupported mind map format type."