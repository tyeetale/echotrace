from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import get_db, create_tables
from services.conversation_service import ConversationService
from services.openai_service import openai_service
from schemas.conversation import (
    Conversation, ConversationCreate, ConversationUpdate, ConversationTree,
    BranchCreate, AddMessageRequest, NodeUpdate, AIResponseRequest, AIResponse
)
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="EchoTrace API",
    description="Branchable AI conversation system API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Conversation endpoints
@app.get("/conversations", response_model=List[Conversation])
async def get_conversations(db: Session = Depends(get_db)):
    """Get all conversations"""
    service = ConversationService(db)
    return service.get_conversations()

@app.post("/conversations", response_model=Conversation)
async def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    service = ConversationService(db)
    return service.create_conversation(conversation_data)

@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific conversation"""
    service = ConversationService(db)
    conversation = service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.get("/conversations/{conversation_id}/tree", response_model=ConversationTree)
async def get_conversation_tree(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get full conversation tree"""
    service = ConversationService(db)
    tree = service.get_conversation_tree(conversation_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return tree

@app.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str,
    update_data: ConversationUpdate,
    db: Session = Depends(get_db)
):
    """Update a conversation"""
    service = ConversationService(db)
    conversation = service.update_conversation(conversation_id, update_data)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    service = ConversationService(db)
    success = service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}

# Branch endpoints
@app.post("/conversations/{conversation_id}/branches")
async def create_branch(
    conversation_id: str,
    branch_data: BranchCreate,
    db: Session = Depends(get_db)
):
    """Create a new branch"""
    service = ConversationService(db)
    branch = service.create_branch(conversation_id, branch_data)
    if not branch:
        raise HTTPException(status_code=404, detail="Conversation or source node not found")
    return branch

# Message endpoints
@app.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str,
    message_data: AddMessageRequest,
    db: Session = Depends(get_db)
):
    """Add a message to the conversation"""
    service = ConversationService(db)
    node = service.add_message(conversation_id, message_data)
    if not node:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return node

@app.put("/conversations/{conversation_id}/nodes/{node_id}")
async def update_node(
    conversation_id: str,
    node_id: str,
    update_data: NodeUpdate,
    db: Session = Depends(get_db)
):
    """Update a node"""
    service = ConversationService(db)
    node = service.update_node(conversation_id, node_id, update_data)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

# AI endpoints
@app.post("/ai/response", response_model=AIResponse)
async def get_ai_response(request: AIResponseRequest):
    """Get AI response from OpenAI"""
    try:
        return await openai_service.get_response(request.messages, request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/models")
async def get_available_models():
    """Get available AI models"""
    return {"models": openai_service.get_available_models()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)