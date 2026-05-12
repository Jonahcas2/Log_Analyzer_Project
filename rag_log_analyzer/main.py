import sys
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from .utils.loaders import load_sop_files
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chains import PebbloRetrievalQA
from langchain_ollama import OllamaLLM

# Directory Input and Validation
try:
    LOG_DIRECTORY = input("-> Enter the path to the log directory: ")
    if not os.path.isdir(LOG_DIRECTORY):
        print(f"Error: Directory not found at'{LOG_DIRECTORY}'")
        sys.exit(1)
except KeyboardInterrupt:
    print("\n\n Exiting...")
    sys.exit(0)

# Document Loading and Processing
try:
    print(f" Loading log files from {LOG_DIRECTORY}...")
    docs = load_sop_files(LOG_DIRECTORY)
    print(f" Loaded {len(docs):,} log entries from {LOG_DIRECTORY}")
except KeyboardInterrupt:
    print("\n\n File loading interrupted by user. Exiting...")
    sys.exit(0)

# Vector Database Creation
print(f" Creating vector database with {len(chunks)} log entries...")
print(" This may take several minutes for large files...")

# Check if database already exists
db_path = "./chroma_db"
db_exists = os.path.exists(db_path)
if db_exists:
    rebuild_choice = input(f" Vector database already exists. Rebuild? (y/n): ").strip().lower()
# Optimized embedding settings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True, 'batch_size': 32}
)
if db_exists and rebuild_choice != 'y':
    print(" Found existing vector database, loading...")
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
else:
    print("Creating a new vector database...")
    db = Chroma.from_documents(
        chunks, embeddings,
        persist_directory=db_path,
        collection_metadata={"hnsw:space": "cosine"}
    )
    print(" Vector database created and saved.")

# RAG Chain Setup
retriever = db.as_retriever()
llm = OllamaLLM(model="mistral")
qa = PebbloRetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, 
    return_source_documents=True
)
