from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
import csv
import os


def load_sop_files(directory: str):
    # Defines supported file extensions
    allowed_exts = ('.log', '.txt', '.out', '.err', '.access', '.json', '.csv', '.yaml', '.yml', '.md', '.asciidoc')

    # Empty list to store doc objects
    docs = []
    
    # Initialized tracking variables
    file_count = 0
    total_lines = 0

    # Process files line by line
    for root, _, files in os.walk(directory):
        for file in files:
            file_lower = file.lower()
            if file_lower.endswith(allowed_exts):
                path = os.path.join(root, file)
                file_count += 1
                print(f" Processing file {file_count}: {file}")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        line_count = 0
                        for i, line in enumerate(f):
                            if line.strip(): # Skip empty lines
                                docs.append(Document(
                                    page_content=line.strip(),
                                    metadata={"source": path, "line_number": i + 1}
                                ))
                                line_count += 1
                                total_lines += 1
                                # Show progress for large files
                                if line_count % 10000 == 0:
                                    print(f"   Completed: {line_count:,} lines procesed")
                except Exception as e:
                    print(f"   Error loading {path}: {e}")
    
    print(f" Summary: Processed {file_count} files, {total_lines:,} total log entries")
    return docs

def _load_csv(path: str):
    docs = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for i, row in enumerate(reader):
            # Embed as "field: value | ..." so context is self-contained
            content = " | ".join(f"{k}: {v}" for k, v in row.items() if v and v.strip())
            if content:
                docs.append(Document(
                    page_content=content,
                    metadata={"source": path, "line_number": i + 2, "columns": ", ".join(headers)}
                ))
                if (i + 1) % 1000 == 0:
                    print(f"   Completed: {i + 1:,} rows processed")
    return docs

def _load_text(path: str):
    docs = []
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if line.strip(): # Skip empty lines
                docs.append(Document(
                    page_content=line.strip(),
                    metadata={"source": path, "line_number": i + 1}
                ))
    return docs