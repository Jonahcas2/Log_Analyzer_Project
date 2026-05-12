def load_sop_files(directory: str):
    # Defines supported file extensions
    allowed_exts = ('.log', '.txt', '.out', '.err', '.access', '.json', '.csv', '.yaml', '.yml', '.md', '.asciidoc')

    # Empty list to store doc objects
    docs = []
    
    # Initialized tracking variables
    file_count = 0
    total_lines = 0