import json
import os


def mock_grounding_service(query: str) -> str:
    """
    Read all txt files from exercises/data/documents and return them in a dictionary.
    
    Args:
        query: The user's question (not used, but required for tool compatibility).
    
    Returns:
        JSON formatted string with all document contents.
    """
    documents = {}
    
    # Get the directory of this file and navigate to exercises/data/documents
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    
    # Navigate up to the workspace root
    docs_path = os.path.join(current_dir, '..', '..', '..', 'exercises', 'data', 'documents')
    docs_path = os.path.abspath(docs_path)
    
    # Read all txt files
    for filename in sorted(os.listdir(docs_path)):
        if filename.endswith('.txt'):
            filepath = os.path.join(docs_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                doc_name = os.path.splitext(filename)[0]
                documents[doc_name] = f.read()
    
    return json.dumps(documents, indent=2)