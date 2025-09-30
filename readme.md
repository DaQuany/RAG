# 🤖 RAG Question-Answering System

A document-based question-answering system using Supabase and the Google Gemini API.

## 🚀 Quick Start

### 1. Check the File Structure
rag-system/
├── main.py              # Backend server
├── index.html           # Frontend
├── requirements.txt     # List of Python packages
├── .env                 # Environment variables (needs to be set up manually)
├── run.py               # Execution script
└── README.md            # This file
```

### 2. Set Environment Variables

Open the `.env` file and enter the following information:

```bash
# Supabase Settings
SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_KEY=your_supabase_anon_key

# Google Gemini API Settings
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Run

```bash
python run.py
```

Or manually:

```bash
# Install packages
pip install -r requirements.txt

# Run the server
python main.py

# Open the index.html file in your browser
```

## ⚙️ Prerequisites

### 1. Supabase Setup

1. Create a project on [Supabase](https://supabase.com)
2. Run the following query in the SQL Editor:

```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create an index for vector search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

3. Enter the project URL and anon key into the .env file.

### 2. Google Gemini API Setup

1. Generate an API key from [Google AI Studio](https://makersuite.google.com/)
2. Enter the API key into the .env file.

## 📱 How to Use

1. **Add Document**: Enter the document content in the upper section and click "Add Document".
2. **Ask a Question**: Enter your question in the chat box at the bottom.
3. **Check the Answer**: The AI will generate an answer based on the uploaded documents.

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python
- **Database**: Supabase (PostgreSQL + pgvector)
- **Embedding**: SentenceTransformers (ko-sroberta-multitask)
- **LLM**: Google Gemini Pro
- **Frontend**: HTML, CSS, JavaScript

## 🔧 Troubleshooting

### Common Errors

1. **Environment Variable Error**
   ```
   ValueError: Environment variables not set
   ```
   → Check the API keys in your .env file.

2. **Supabase Connection Error**
   ```
   supabase connection failed
   ```
   → Verify that the Supabase URL and key are correct and that the tables have been created.

3. **Gemini API Error**
   ```
   google.generativeai.types.generation_types.BlockedPromptException
   ```
   →  Check if the API key is valid and if the request complies with the usage policies.

4. **CORS Error**
   ```
   Access to fetch at 'http://localhost:8000' from origin 'file://' has been blocked
   ```
   → Make sure the backend server is running.

## 📞 Support

If you encounter a problem:
1. Check the error message in the terminal.
2. Re-check the .env file settings.
3. Check the table creation status on the Supabase dashboard.
4. Check for network errors in the browser's developer tools.

## 📈 Potential Enhancements

- Add file upload functionality
- User authentication system
- Save chat history
- Manage multiple document collections
- Support for PDF, Word files