import pandas as pd
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from tqdm import tqdm  # for progress bar

# ------------------ LOAD TEXT ------------------
loader = TextLoader("tagged_description.txt", encoding="utf-8")
documents = loader.load()
print(f"Loaded {len(documents)} documents.")

# ------------------ SPLIT DOCUMENTS ------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)
print(f"Split into {len(docs)} chunks.")

# ------------------ EMBEDDING MODEL ------------------
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
print("Embedding model loaded.")

# ------------------ CREATE DB ------------------
# Chroma now automatically saves to persist_directory
db = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="db"
)

print("DB created and saved successfully.")