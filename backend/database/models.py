from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    current_branch_id = Column(String, ForeignKey("branches.id"), nullable=True)
    current_node_id = Column(String, ForeignKey("nodes.id"), nullable=True)
    
    # Relationships
    branches = relationship("Branch", back_populates="conversation", cascade="all, delete-orphan")
    nodes = relationship("Node", back_populates="conversation", cascade="all, delete-orphan")

class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    root_node_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    node_ids = Column(JSON, nullable=False, default=list)  # List of node IDs in order
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="branches")
    root_node = relationship("Node", foreign_keys=[root_node_id])

class Node(Base):
    __tablename__ = "nodes"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    user_msg = Column(Text, nullable=True)
    ai_msg = Column(Text, nullable=True)
    parent_id = Column(String, ForeignKey("nodes.id"), nullable=True)
    annotations = Column(Text, nullable=True, default="")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="nodes")
    parent = relationship("Node", remote_side=[id], backref="children")