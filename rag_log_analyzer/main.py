import sys
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from .utils.loaders import load_sop_files
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chains import PebbloRetrievalQA
from langchain_ollama import OllamaLLM

try:
    LOG_DIRECTORY = input("-> Enter the path to the log directory: ")
    if not os.path.isdir(LOG_DIRECTORY):
        print(f"Error: Directory not found at'{LOG_DIRECTORY}'")
        sys.exit(1)
except KeyboardInterrupt:
    print("\n\n Exiting...")
    sys.exit(0)

try:
    print(f" Loading log files from {LOG_DIRECTORY}...")
    docs = load_sop_files(LOG_DIRECTORY)
    print(f" Loaded {len(docs):,} log entries from {LOG_DIRECTORY}")
except KeyboardInterrupt:
    print("\n\n File loading interrupted by user. Exiting...")
    sys.exit(0)