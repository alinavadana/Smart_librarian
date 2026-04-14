# Smart Librarian

## Project Overview

Smart Librarian is an AI-powered book recommendation chatbot built with **OpenAI GPT + RAG + ChromaDB**.  
The application recommends books based on the user's interests, retrieves semantically relevant results from a vector database, and then shows a full summary for the selected title using a local summary tool.

The project also includes three different chatbot personalities:
- a **main storyteller bot** that recommends the book in a creative way
- **Steven**, a grumpy bot who explains what someone might dislike about the book
- **Crispy**, an enthusiastic bot who highlights what is exciting and worth reading

The user interacts with the app through a **Streamlit interface**, with conversation history, language selection, and a moderation flow for offensive language.

---

## Features

- Book recommendation based on semantic search
- Local vector store using **ChromaDB**
- OpenAI embeddings with `text-embedding-3-small`
- Conversational recommendation flow powered by GPT
- Three AI personalities:
  - Storyteller
  - Steven (grumpy)
  - Crispy (enthusiastic)
- Full book summary retrieval with `get_summary_by_title(title)`
- Offensive language detection
- Special Steven full-screen warning overlay for rude input
- Streamlit chat-style UI
- Persistent conversation history saved locally
- Language selection: **Romanian / English**

---

## Tech Stack

- **Python**
- **Streamlit**
- **OpenAI API**
- **ChromaDB**
- **python-dotenv**
- **JSON** for local data storage

---

## Project Structure

```text
Smart_Librarian/
├── README.md
├── app.py
├── requirements.txt
├── .env
├── chroma_db/                  # created automatically after indexing
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

---------

## Requirement Coverage

This project covers the main requirements of the assignment:

- A local book summary dataset with 10+ books
- ChromaDB used as a local vector store
- OpenAI embeddings for semantic search
- A recommendation chatbot built with GPT
- A local summary retrieval tool: `get_summary_by_title(title)`
- Three chatbot personalities:
  - Storyteller
  - Steven
  - Crispy
- Offensive language moderation
- Streamlit interface with persistent conversation history

## Deliverables

The delivered project includes:

- `data/book_summaries.json`
- Python source code
- ChromaDB indexing and semantic retrieval
- `get_summary_by_title()` tool
- Streamlit UI
- Persistent local conversation history
- README with setup and usage instructions

## Limitations

Current limitations of the project:

- `get_summary_by_title()` is implemented as a local Python function, not as full OpenAI function-calling schema
- Audio / TTS is not included in the final version
- The UI is built in Streamlit, so some advanced frontend effects are limited compared to React

## Demo Flow

A typical interaction looks like this:

1. The user enters a book request
2. The app retrieves the most relevant books from ChromaDB
3. The best match is selected
4. The storyteller recommends the book
5. Steven gives counterarguments
6. Crispy gives enthusiastic arguments
7. The full summary is shown
8. The conversation is saved in history

## Setup and Installation

### 1. Create a virtual environment

#### Windows
```bash
py -m venv venv
venv\Scripts\activate

#### Mac/Linux
python3 -m venv venv
source venv/bin/activate

#Install dependencies
pip install openai chromadb streamlit python-dotenv

#Optional: save dependencies
pip freeze > requirements.txt

##Environment Variables

Create a file named .env in the root of the project:

OPENAI_API_KEY=your_openai_api_key_here

#How to Run the App

Run the Streamlit application with:

streamlit run app.py

If that does not work, try:
python -m streamlit run app.py


#Example Prompts

I want a book about friendship and magic
Recommend a book about freedom and social control
What should I read if I enjoy war stories?
I want something romantic and emotional
What is 1984?

