from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base schemas
class NodeBase(BaseModel):
    user_msg: Optional[str] = None
    ai_msg: Optional[str] = None
    parent_id: Optional[str] = None
    annotations: Optional[str] = ""

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    user_msg: Optional[str] = None
    ai_msg: Optional[str] = None
    annotations: Optional[str] = None

class Node(NodeBase):
    id: str
    conversation_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BranchBase(BaseModel):
    name: str
    root_node_id: str

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: str
    conversation_id: str
    node_ids: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    current_branch_id: Optional[str] = None
    current_node_id: Optional[str] = None

class Conversation(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    current_branch_id: Optional[str] = None
    current_node_id: Optional[str] = None
    
    class Config:
        from_attributes = True

# Complex schemas
class ConversationTree(BaseModel):
    conversation: Conversation
    branches: List[Branch]
    nodes: List[Node]
    current_branch: Optional[Branch] = None
    current_node: Optional[Node] = None

# Request schemas
class CreateBranchRequest(BaseModel):
    name: str
    from_node_id: str

class AddMessageRequest(BaseModel):
    user_msg: str
    parent_id: str

class AIResponseRequest(BaseModel):
    messages: List[dict]
    model: Optional[str] = "gpt-4"

class AIResponse(BaseModel):
    content: str
    model: str