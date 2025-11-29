import json
from uuid import uuid4
from pathlib import Path
from datetime import datetime

class Node:
    def __init__(self, user_msg, ai_msg, parent_id=None, node_id=None, annotations=None, timestamp=None):
        self.id = node_id or str(uuid4())
        self.user_msg = user_msg
        self.ai_msg = ai_msg
        self.parent_id = parent_id
        self.annotations = annotations or ""
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "user_msg": self.user_msg,
            "ai_msg": self.ai_msg,
            "parent_id": self.parent_id,
            "annotations": self.annotations,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data):
        return Node(
            user_msg=data["user_msg"],
            ai_msg=data["ai_msg"],
            parent_id=data["parent_id"],
            node_id=data["id"],
            annotations=data.get("annotations", ""),
            timestamp=data.get("timestamp"),
        )

class Branch:
    def __init__(self, name, root_node_id, branch_id=None, node_ids=None, created_at=None):
        self.id = branch_id or str(uuid4())
        self.name = name
        self.root_node_id = root_node_id
        self.node_ids = node_ids or [root_node_id]
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "root_node_id": self.root_node_id,
            "node_ids": self.node_ids,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Branch(
            name=data["name"],
            root_node_id=data["root_node_id"],
            branch_id=data["id"],
            node_ids=data["node_ids"],
            created_at=data.get("created_at"),
        )

class NodeManager:
    def __init__(self, storage_path):
        self.path = Path(storage_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.nodes = {}
        self.current_node_id = None
        self.branches = {}
        self.current_branch_id = None
        self.load()

    def save(self):
        data = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "current_node_id": self.current_node_id,
            "branches": [b.to_dict() for b in self.branches.values()],
            "current_branch_id": self.current_branch_id,
        }
        self.path.write_text(json.dumps(data, indent=2))

    def load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
            except Exception:
                data = {}
            self.nodes = {n["id"]: Node.from_dict(n) for n in data.get("nodes", [])}
            self.current_node_id = data.get("current_node_id")
            self.branches = {b["id"]: Branch.from_dict(b) for b in data.get("branches", [])}
            self.current_branch_id = data.get("current_branch_id")
        # Guarantee at least one node and one branch always
        if not self.nodes:
            root = Node("Start your conversation...", "Hi! How can I help you?")
            self.nodes[root.id] = root
            self.current_node_id = root.id
        if not self.branches:
            branch = Branch("main", self.current_node_id)
            self.branches[branch.id] = branch
            self.current_branch_id = branch.id
        # Make sure root node is included in branch
        if not self.branches[self.current_branch_id].node_ids:
            self.branches[self.current_branch_id].node_ids = [self.current_node_id]
        self.save()

    def add_node(self, user_msg, ai_msg, parent_id):
        node = Node(user_msg, ai_msg, parent_id)
        self.nodes[node.id] = node
        branch = self.branches[self.current_branch_id]
        branch.node_ids.append(node.id)
        self.current_node_id = node.id
        self.save()
        return node

    def create_branch_from(self, branch_name, from_node_id):
        branch = self.branches[self.current_branch_id]
        if from_node_id not in branch.node_ids:
            return None
        idx = branch.node_ids.index(from_node_id)
        ancestor_ids = branch.node_ids[:idx+1]
        new_branch = Branch(branch_name, ancestor_ids[0], node_ids=ancestor_ids.copy())
        self.branches[new_branch.id] = new_branch
        self.current_branch_id = new_branch.id
        self.current_node_id = from_node_id
        self.save()
        return new_branch

    def get_all_nodes(self):
        return list(self.nodes.values())

    def get_branch_timeline_nodes(self, branch_id=None):
        branch = self.branches[branch_id or self.current_branch_id]
        return [self.nodes[nid] for nid in branch.node_ids]