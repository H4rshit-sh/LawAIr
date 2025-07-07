# libraries
import json
import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import google.generativeai as genai

with open('ipc.json','r', encoding='utf-8') as f:
    ipc = json.load(f)


# create list of documents
documents = []

for sec in ipc:
    text = f"Section {sec['Section']}: {sec['section_title']} \n {sec['section_desc']}"
    documents.append(Document(page_content=text, metadata={'section': sec['Section']}))

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embedding)

vectorstore.save_local("vectorstore")

# API setup
genai.configure(api_key=("AIzaSyBSJtBrvboEoXGBL5U6eZHIQLy_r1r-ka8"))

vectorstore = FAISS.load_local("vectorstore", embedding , allow_dangerous_deserialization=True)

query = input("\n Enter your legal question: ").strip()

result = vectorstore.similarity_search(query)

context = "\n\n".join([r.page_content for r in result])

prompt = f"""
you are a AI lawyer, trained on Indian Penal Code (IPC). Based on the following sections of law, answer the user's question clearly and concisely

Law Sections: {context}
Question: {query}
Answer:
"""
model = genai.GenerativeModel("gemini-2.5-pro")

print("\n🤖 Thinking...\n")

response = model.generate_content(prompt, stream=True)

print("\n🤖 LawAIr:\n")
for chunk in response:
    print(chunk.text, end="", flush=True)

    print()

