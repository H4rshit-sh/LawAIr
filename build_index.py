import os
import json
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

documents = []

law_files = {
    "ipc.json": "Indian Penal Code",
    "crpc.json": "Code of Criminal Procedure",
    "cpc.json": "Civil Procedure Code",
    "iea.json": "Indian Evidence Act",
    "MVA.json": "Motor Vehicles Act"
}

for file,act in law_files.items():
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for sec in data:
        section = sec.get("Section")  
        title = sec.get("section_title") 
        desc = sec.get("section_desc")

        text = f"Section {section} : {title}\n\n{desc}"
        documents.append(Document(page_content=text, metadata={"section": section,
                "title": title,
                "act": act,
                "source_file": file }))

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embedding)
vectorstore.save_local("vectorstore")
print("✅ Vectorstore built and saved!")
