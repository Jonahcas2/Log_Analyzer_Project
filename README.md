# rag-log-analyzer

A local, privacy-first RAG (Retrieval-Augmented Generation) tool for querying log files in plain English. Instead of grepping through thousands of lines, just ask a question and get a summarized, source-attributed answer — powered by a local LLM with no data leaving your machine.

---

## How It Works

1. Log files are loaded line-by-line from a directory you specify
2. Each line is embedded using `sentence-transformers/all-MiniLM-L6-v2` and stored in a local ChromaDB vector database
3. When you ask a question, the most relevant log entries are retrieved via cosine similarity
4. A local Mistral LLM (via Ollama) synthesizes those entries into a concise answer, with source file and line number attribution

---

## Project Structure

```
Log_Analyzer_Project/
├── archive/                    # Place your log files here
│   └── Incident_response.txt   # Example: incident field reference
├── rag_log_analyzer/
│   ├── main.py                 # Entry point
│   ├── requirements.txt        # Python dependencies
│   └── utils/
│       └── loaders.py          # File loading and document processing
├── chroma_db/                  # Auto-generated vector database (gitignored)
├── .gitignore
└── README.md
```

> **Note:** Place all log files you want to analyze inside the `archive/` folder. The tool will recursively scan it and process any supported file type.

---

## Supported File Types

`.log` `.txt` `.out` `.err` `.access` `.json` `.csv` `.yaml` `.yml` `.md` `.asciidoc`

---

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally with the Mistral model pulled:

```bash
ollama pull mistral
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/your-username/Log_Analyzer_Project.git
cd Log_Analyzer_Project/rag_log_analyzer

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
cd rag_log_analyzer
python main.py
```

You'll be prompted to enter the path to your log directory. Point it at the `archive/` folder (or any directory containing your logs):

```
-> Enter the path to the log directory: ../archive
```

The tool will process your files, build (or load) the vector database, and drop you into an interactive query loop:

```
You (e.g. 'What errors occurred in the last hour?'): What are the most common failure types?
 Assistant:
 Based on the log entries, the most common failure types are...

 Sources:
 - ../archive/Incident_response.txt (Line 42)
 - ../archive/system.log (Line 1087)
```

Type `exit` or `quit` to close the tool.

---

## Vector Database Caching

The ChromaDB database is saved to `./chroma_db/` after the first run. On subsequent runs you'll be asked whether to reuse or rebuild it — rebuilding is only necessary if your log files have changed.

The `chroma_db/` directory is gitignored and will not be committed to version control.

---

## Dependencies

| Package | Purpose |
|---|---|
| `langchain` | RAG chain orchestration |
| `langchain-community` | Document loaders and HuggingFace embeddings |
| `langchain-ollama` | Local LLM integration via Ollama |
| `chromadb` | Local vector database |
| `sentence-transformers` | Text embedding model |

---

## Privacy

This tool runs entirely locally. Your log files are embedded and stored on disk in `chroma_db/`, and all inference is handled by Ollama. No data is sent to any external API or service.

---

## License

MIT
