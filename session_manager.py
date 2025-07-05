import os
import json
from uuid import uuid4
from pathlib import Path

DATA_DIR = Path("data/conversations")

class SessionManager:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.sessions = self._scan_sessions()

    def _scan_sessions(self):
        return sorted([f for f in self.data_dir.glob("*.json")])

    def list_sessions(self):
        files = self._scan_sessions()
        # Try to extract "title" or use filename
        sessions = []
        for f in files:
            title = f"Conversation {f.stem[-8:]}"
            try:
                with open(f) as fh:
                    data = json.load(fh)
                    # Use first node preview as title if possible
                    first = data.get("nodes", [{}])[0].get("user_msg", '')
                    if first:
                        title = (first[:20] + "...") if len(first) > 23 else first
            except Exception: pass
            sessions.append({"id": f.stem, "filename": f, "title": title})
        return sessions

    def create_session(self):
        uid = "conv_" + str(uuid4())[:8]
        fn = self.data_dir / (uid + ".json")
        # Actually create the file!
        with open(fn, "w") as f:
            json.dump({"nodes": [], "branches": []}, f)
        return fn