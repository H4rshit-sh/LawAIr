
# ⚖️ LawAIr – AI-Powered Indian Legal Assistant

**LawAIr** is an intelligent legal assistant that uses state-of-the-art AI (RAG architecture) to answer legal questions based on various Indian legal codes like the IPC, CrPC, CPC, IEA, MVA, and more. It empowers users—students, researchers, or citizens—to interact with the law in natural language.

---

## 🚀 Features

- ✅ Ask natural-language legal questions
- 🔍 Retrieves relevant sections from multiple Indian legal acts
- 💡 AI-powered answers with contextual understanding
- 🧠 RAG architecture (Retrieval-Augmented Generation)
- 🖥️ Chatbot-style web interface via Streamlit
- 📚 Built on publicly available bare act JSON data

---

## 📂 Supported Legal Acts

- Indian Penal Code, 1860 (IPC)
- Code of Criminal Procedure, 1973 (CrPC)
- Civil Procedure Code, 1908 (CPC)
- Indian Evidence Act, 1872 (IEA)
- Motor Vehicles Act, 1988 (MVA)

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, FAISS (vector DB), LangChain
- **Embeddings**: HuggingFace (MiniLM)
- **LLM**: Gemini Pro (Google Generative AI API)
- **RAG**: Retrieval-Augmented Generation pipeline

---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/LawAIr.git
cd LawAIr
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Add Your Gemini API Key
Replace the API key in `main.py`:
```python
genai.configure(api_key="YOUR_API_KEY")
```

### 4. ⚡ Build the Vector Index
Run the `build_index.py` script to convert the law JSONs into searchable vector chunks:
```bash
python build_index.py
```

This will create a folder named `vectorstore/` that holds the FAISS index.

### 5. ▶️ Run the Web App
Now start the chatbot interface:
```bash
streamlit run main.py
```

---

## 📸 UI Preview

<img src="screenshot.png" width="600">

---

## 📁 Directory Structure

```
LawAIr/
├── main.py              # Streamlit UI & query pipeline
├── build_index.py       # Builds FAISS vectorstore from legal JSONs
├── vectorstore/         # Saved FAISS DB (after running build_index)
├── ipc.json             # Legal text files
├── crpc.json
├── ...
└── README.md
```

---

## 🧠 Limitations

- Responses limited to the acts currently ingested
- Not a replacement for legal advice or a certified lawyer
- May miss context in complex legal scenarios

---

## 💡 Future Improvements

- Add support for more Indian Acts (e.g., Hindu Succession Act, RTI Act)
- Upload PDFs / case laws as context
- Multilingual support (Hindi, regional languages)
- Export answers as PDF/legal brief

---

## 📜 Disclaimer

> LawAIr is an educational and informational tool. It does not provide legal advice and should not be used as a substitute for professional legal consultation.

---

## 🧑‍🎓 Author

**Harshit Sharma**  
B.Tech IT, Maharaja Surajmal Institute of Technology  
GitHub: [@yourusername](https://github.com/yourusername)
