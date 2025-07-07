# build_index.py
import json
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

with open('ipc.json', 'r', encoding='utf-8') as f:
    ipc = json.load(f)

documents = []
for sec in ipc:
    text = f"Section {sec['Section']}: {sec['section_title']}\n{sec['section_desc']}"
    documents.append(Document(page_content=text, metadata={'section': sec['Section']}))

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embedding)
vectorstore.save_local("vectorstore")
print("✅ Vectorstore built and saved!")
