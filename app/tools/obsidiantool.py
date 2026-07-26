from langchain_core.tools import tool
from langchain_community.document_loaders import ObsidianLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.agents import create_agent

from pathlib import Path

# --- Step 1: Pre-initialize the Retriever (Do this once, outside the tool) ---
# This prevents reloading your entire vault on every single agent loop.
# loader = ObsidianLoader("C:\\Users\\ronjo\\Documents\\Obsidian Vaults\\ron")

# current_dir = Path(__file__).resolve().parent
current_dir = Path.cwd()
vault_path = current_dir / "data/vault"

loader = ObsidianLoader(str(vault_path))
documents = loader.load()

text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# --- Step 2: Define the Custom Tool ---
@tool("search_obsidian_notes", description="Used to search through my obsidian personal knowledge base or notes vault.")
def search_obsidian_notes(query: str) -> str:
    """
    Search your local Obsidian personal knowledge base or notes vault. 
    Use this tool whenever you need context about personal schedules, goals, 
    journals, project notes, or user-specific facts. Input should be a search query string.
    """
    # Fetch relevant chunks from the local database
    docs = retriever.invoke(query)
    
    # Format results to return a clean string payload to the orchestrator agent
    formatted_docs = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown Note")
        formatted_docs.append(f"--- From Note: {source} ---\n{doc.page_content}")
        
    return "\n\n".join(formatted_docs)


# Need to comment out the @tool() decorator if calling directly
if __name__ == "__main__":
   print(search_obsidian_notes("What is the first item on my ToDo list"))
