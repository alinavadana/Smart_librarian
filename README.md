<div align="center">

# 📚 Smart Librarian

**AI-powered book recommendation app built with OpenAI GPT, RAG, and ChromaDB**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-black?logo=openai)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)

</div>

---

## ✨ Overview

**Smart Librarian** is an AI-powered book recommendation chatbot that combines **OpenAI GPT**, **Retrieval-Augmented Generation (RAG)**, and **ChromaDB** to recommend books based on the user’s interests.

The app performs **semantic search** over a local dataset of book summaries, retrieves the most relevant result from the vector store, and then enriches the answer with a **full summary** using a local tool.

It also includes three chatbot personalities:

- **Storyteller** — the main bot that recommends the book in a creative and conversational way
- **Steven** — a grumpy bot that points out possible downsides of the recommendation
- **Crispy** — an enthusiastic bot that highlights what makes the book exciting and worth reading

The project also includes:
- offensive language moderation
- persistent conversation history
- language selection (**Romanian / English**)
- a Streamlit chat-style interface

---

## 🚀 Features

- Semantic book recommendation based on user interests
- Local vector database using **ChromaDB**
- OpenAI embeddings with `text-embedding-3-small`
- Conversational responses powered by GPT
- Three different chatbot personalities
- Full summary retrieval with `get_summary_by_title(title)`
- Offensive language detection and Steven warning overlay
- Persistent local conversation history
- Chat-like Streamlit UI
- Language switch between **Romanian** and **English**

---

## 🧠 How It Works

1. The user enters a request such as:
   - *I want a book about friendship and magic*
   - *Recommend a book about freedom and social control*

2. The app converts the query into an embedding using OpenAI.

3. That embedding is compared against book documents stored in **ChromaDB**.

4. The most relevant book is selected.

5. The full summary is retrieved with the local tool:

   ```python
   get_summary_by_title(title: str)

6.  Three responses are generated:
     -Storyteller explains why the book matches the request
     -Steven gives humorous counterarguments
     -Crispy gives enthusiastic praise
    
7.  The conversation is shown in the UI and saved in local history.

## 🗂️ Project Structure
Smart_Librarian/
├── README.md
├── app.py
├── requirements.txt
├── .env
├── chroma_db/
│
├── data/
│   ├── book_summaries.json
│   └── conversations.json
│
└── src/
    ├── bots.py
    ├── history.py
    ├── moderation.py
    ├── recommender.py
    ├── tools.py
    └── vector_store.py

  ## 🛠️ Tech Stack
    -Python
    -Streamlit
    -OpenAI API
    -ChromaDB
    -python-dotenv
    -JSON for local storage

  ## 📦 Deliverables

    The project includes:
    
    -data/book_summaries.json
    -Python source code
    -ChromaDB indexing and semantic retrieval
    -get_summary_by_title() tool
    -Streamlit UI
    -Persistent local conversation history
    -README with setup and usage instructions

   ## 🧪 Setup and Installation
1. Create a virtual environment
### Windows:
py -m venv venv
venv\Scripts\activate
### Mac / Linux
python3 -m venv venv
source venv/bin/activate

2. Install dependencies
pip install openai chromadb streamlit python-dotenv

4. Optional: save dependencies
pip freeze > requirements.txt


  ## 🔐 Environment Variables

Create a file named .env in the root of the project:

OPENAI_API_KEY=your_openai_api_key_here
 
 
  ## ▶️ How to Run the App

Run the Streamlit app with:

streamlit run app.py

If that does not work, try:

python -m streamlit run app.py


  ## 💬 Example Prompts
I want a book about friendship and magic
Recommend a book about freedom and social control
What should I read if I enjoy war stories?
I want something romantic and emotional
What is 1984?

 ## 🧭 Demo Flow

A typical interaction looks like this:

The user enters a book request
The app retrieves the most relevant books from ChromaDB
The best match is selected
The Storyteller recommends the book
Steven gives counterarguments
Crispy gives enthusiastic arguments
The full summary is shown
The conversation is saved in history

 ## 📘 Summary

Smart Librarian demonstrates:

semantic retrieval with RAG
local vector storage with ChromaDB
GPT-based response generation
multi-personality chatbot design
local summary retrieval
moderation and persistent UI interaction

It was designed to stay simple enough to understand, while still demonstrating the full flow of an AI-powered recommendation assistant.
