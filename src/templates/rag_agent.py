"""RAG Agent template with LangChain and Streamlit"""
from rich.console import Console
from .base import ProjectTemplate

console = Console()


class RAGAgentTemplate(ProjectTemplate):
    """Template for RAG Agent with LangChain"""
    
    name = "RAG Agent"
    description = "LangChain-based RAG agent with Streamlit UI, Qdrant, and Ollama"
    
    def generate(self):
        console.print("[cyan]Creating RAG Agent project...[/cyan]")
        
        # Create folders
        self.create_folder_structure(["src", "src/agents", "src/vectorstore", "streamlit_app"])
        
        # Dependencies (without extra quotes)
        deps = [
            '"langchain>=0.1.0"',
            '"langchain-community>=0.0.20"',
            '"streamlit>=1.29.0"',
            '"qdrant-client>=1.7.0"',
            '"ollama>=0.1.0"',
            '"python-dotenv>=1.0.0"',
            '"sentence-transformers>=2.2.0"',
        ]
        self.create_pyproject_toml(deps)
        
        # Create main app structure
        self._create_streamlit_app()
        self._create_agent_module()
        self._create_data_generation_script()
        self._create_env_example()
        self.create_src_init()
        
        # Create README
        readme = f'''# {self.project_name}

A RAG (Retrieval-Augmented Generation) agent built with LangChain and Streamlit.

## Setup

1. Install dependencies using uv:
```bash
uv sync
```

2. Copy `.env.example` to `.env` and configure your settings

3. Run the Streamlit app:
```bash
uv run streamlit run streamlit_app/app.py
```

## Project Structure

- `src/agents/` - Agent implementations
- `src/vectorstore/` - Vector database configuration
- `streamlit_app/` - Streamlit frontend
- `scripts/` - Utility scripts including data generation
- `notebooks/` - Jupyter notebooks for experimentation
- `data/` - Data storage
- `tests/` - Test suite

## Testing

Run tests with:
```bash
uv run pytest
```

## Architecture

This RAG agent uses:
- **LangChain** for agent orchestration
- **Qdrant** for vector storage
- **Ollama** for local LLM inference
- **Streamlit** for the web interface
'''
        self.create_readme(readme)
        self.create_gitignore()
        self.create_basic_test()
        
        console.print("[green]✓ RAG Agent project created successfully![/green]")
    
    def _create_streamlit_app(self):
        content = '''import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

st.set_page_config(page_title="RAG Agent", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🤖 RAG Agent")
    st.markdown("---")
    
    # Configuration options
    st.subheader("Configuration")
    model = st.selectbox("Model", ["llama2", "mistral", "codellama"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response (placeholder)
    with st.chat_message("assistant"):
        response = f"Echo: {prompt}"  # Replace with actual agent logic
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
'''
        with open(self.project_path / "streamlit_app" / "app.py", "w") as f:
            f.write(content)
    
    def _create_agent_module(self):
        content = '''"""RAG Agent implementation"""
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from typing import Optional


class RAGAgent:
    """Main RAG Agent class"""
    
    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name
        self.vectorstore: Optional[Qdrant] = None
        
    def initialize_vectorstore(self, collection_name: str):
        """Initialize Qdrant vector store"""
        # TODO: Implement Qdrant initialization
        pass
    
    def query(self, question: str) -> str:
        """Query the RAG agent"""
        # TODO: Implement query logic
        return f"Response to: {question}"
'''
        with open(self.project_path / "src" / "agents" / "rag_agent.py", "w") as f:
            f.write(content)
        
        (self.project_path / "src" / "agents" / "__init__.py").touch()
    
    def _create_data_generation_script(self):
        content = '''#!/usr/bin/env python3
"""
Data generation script for creating synthetic data for the RAG system
"""
import json
from pathlib import Path


def generate_sample_documents(num_docs: int = 10):
    """Generate sample documents for testing"""
    documents = []
    
    for i in range(num_docs):
        doc = {
            "id": f"doc_{i}",
            "content": f"This is sample document {i} with some content.",
            "metadata": {
                "source": "generated",
                "index": i
            }
        }
        documents.append(doc)
    
    return documents


def main():
    """Main function"""
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    documents = generate_sample_documents()
    
    output_file = output_dir / "sample_documents.json"
    with open(output_file, "w") as f:
        json.dump(documents, f, indent=2)
    
    print(f"Generated {len(documents)} documents -> {output_file}")


if __name__ == "__main__":
    main()
'''
        with open(self.project_path / "scripts" / "generate_data.py", "w") as f:
            f.write(content)
    
    def _create_env_example(self):
        content = '''# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Model Settings
DEFAULT_MODEL=llama2
EMBEDDING_MODEL=all-MiniLM-L6-v2
'''
        with open(self.project_path / ".env.example", "w") as f:
            f.write(content)

