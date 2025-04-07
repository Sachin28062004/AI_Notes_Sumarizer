def generate_mindmap(text):
    """
    Generate a simple mindmap-style representation from text.
    
    Args:
        text: Input text
    
    Returns:
        A string representing the mindmap
    """
    sentences = text.split('. ')
    if not sentences:
        return "No content to generate mindmap."
    
    central_node = sentences[0]
    branches = sentences[1:] if len(sentences) > 1 else ["No additional points."]
    
    mindmap = f"Central Idea: {central_node}\n"
    for i, branch in enumerate(branches, 1):
        mindmap += f"Branch {i}: {branch}\n"
    
    return mindmap
