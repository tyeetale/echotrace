from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.models import Conversation, Branch, Node
from ..schemas.conversation import (
    ConversationCreate, ConversationUpdate, BranchCreate, NodeCreate, NodeUpdate,
    ConversationTree
)
import uuid
from datetime import datetime

class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        conversation_id = str(uuid.uuid4())
        
        conversation = Conversation(
            id=conversation_id,
            title=conversation_data.title
        )
        
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        # Create initial node and branch
        self._create_initial_structure(conversation_id)
        
        return conversation

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_conversations(self) -> List[Conversation]:
        """Get all conversations"""
        return self.db.query(Conversation).order_by(Conversation.updated_at.desc()).all()

    def update_conversation(self, conversation_id: str, update_data: ConversationUpdate) -> Optional[Conversation]:
        """Update a conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(conversation, field, value)
        
        conversation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        
        self.db.delete(conversation)
        self.db.commit()
        return True

    def get_conversation_tree(self, conversation_id: str) -> Optional[ConversationTree]:
        """Get full conversation tree"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        branches = self.db.query(Branch).filter(Branch.conversation_id == conversation_id).all()
        nodes = self.db.query(Node).filter(Node.conversation_id == conversation_id).all()
        
        current_branch = None
        current_node = None
        
        if conversation.current_branch_id:
            current_branch = next((b for b in branches if b.id == conversation.current_branch_id), None)
        
        if conversation.current_node_id:
            current_node = next((n for n in nodes if n.id == conversation.current_node_id), None)
        
        return ConversationTree(
            conversation=conversation,
            branches=branches,
            nodes=nodes,
            current_branch=current_branch,
            current_node=current_node
        )

    def create_branch(self, conversation_id: str, branch_data: BranchCreate) -> Optional[Branch]:
        """Create a new branch from a specific node"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        # Find the source branch and node
        source_branch = None
        for branch in conversation.branches:
            if branch.node_ids and branch_data.from_node_id in branch.node_ids:
                source_branch = branch
                break
        
        if not source_branch:
            return None
        
        # Create new branch
        branch_id = str(uuid.uuid4())
        node_index = source_branch.node_ids.index(branch_data.from_node_id)
        ancestor_ids = source_branch.node_ids[:node_index + 1]
        
        branch = Branch(
            id=branch_id,
            name=branch_data.name,
            conversation_id=conversation_id,
            root_node_id=branch_data.from_node_id,
            node_ids=ancestor_ids.copy()
        )
        
        self.db.add(branch)
        
        # Update conversation's current branch and node
        conversation.current_branch_id = branch_id
        conversation.current_node_id = branch_data.from_node_id
        conversation.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(branch)
        
        return branch

    def add_message(self, conversation_id: str, message_data: AddMessageRequest) -> Optional[Node]:
        """Add a new message to the current branch"""
        conversation = self.get_conversation(conversation_id)
        if not conversation or not conversation.current_branch_id:
            return None
        
        # Create new node
        node_id = str(uuid.uuid4())
        node = Node(
            id=node_id,
            conversation_id=conversation_id,
            user_msg=message_data.user_msg,
            parent_id=message_data.parent_id
        )
        
        self.db.add(node)
        
        # Add to current branch
        current_branch = self.db.query(Branch).filter(Branch.id == conversation.current_branch_id).first()
        if current_branch:
            current_branch.node_ids.append(node_id)
            current_branch.updated_at = datetime.utcnow()
        
        # Update conversation's current node
        conversation.current_node_id = node_id
        conversation.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(node)
        
        return node

    def update_node(self, conversation_id: str, node_id: str, update_data: NodeUpdate) -> Optional[Node]:
        """Update a node"""
        node = self.db.query(Node).filter(
            Node.id == node_id,
            Node.conversation_id == conversation_id
        ).first()
        
        if not node:
            return None
        
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(node, field, value)
        
        node.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(node)
        
        return node

    def _create_initial_structure(self, conversation_id: str):
        """Create initial node and branch for a new conversation"""
        # Create initial node
        node_id = str(uuid.uuid4())
        initial_node = Node(
            id=node_id,
            conversation_id=conversation_id,
            user_msg="Start your conversation...",
            ai_msg="Hi! How can I help you?"
        )
        
        self.db.add(initial_node)
        
        # Create main branch
        branch_id = str(uuid.uuid4())
        main_branch = Branch(
            id=branch_id,
            name="main",
            conversation_id=conversation_id,
            root_node_id=node_id,
            node_ids=[node_id]
        )
        
        self.db.add(main_branch)
        
        # Update conversation
        conversation = self.get_conversation(conversation_id)
        conversation.current_branch_id = branch_id
        conversation.current_node_id = node_id
        
        self.db.commit()