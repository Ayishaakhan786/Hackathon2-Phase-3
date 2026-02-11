from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import contextmanager
from dotenv import load_dotenv
import os
import bleach
from openai import OpenAI
from datetime import datetime
import uuid

from .database_py import engine
from .session import get_session
from .models_py import ChatLog, ChatLogCreate, ChatLogRead

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI app
app = FastAPI(title="GIAIC Chat API", version="1.0.0")

# Add CORS middleware to allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session

# Startup event to create tables
@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

# Chat endpoint
@app.post("/chat", response_model=ChatLogRead)
def chat(chat_data: ChatLogCreate, session: Session = Depends(get_session)):
    try:
        # Sanitize user input
        sanitized_message = bleach.clean(chat_data.user_message)
        
        # Generate conversation ID if not provided
        conversation_id = chat_data.conversation_id or str(uuid.uuid4())
        
        # Create message for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": sanitized_message}
        ]
        
        # Call OpenAI API using v1.0+ format
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as suggested
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract AI response
        ai_response = response.choices[0].message.content
        
        # Create chat log instance
        chat_log = ChatLog(
            user_message=sanitized_message,
            ai_response=ai_response,
            conversation_id=conversation_id
        )
        
        # Save to database
        session.add(chat_log)
        session.commit()
        session.refresh(chat_log)
        
        return chat_log
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error in chat endpoint: {str(e)}")
        
        # Return a structured error response
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)