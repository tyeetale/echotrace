# 🔁 EchoTrace

**EchoTrace** is a branchable, version-controlled AI conversation system — like Git for dialogue.

Built with **Python** and **Streamlit**, EchoTrace lets you fork conversations at any point, explore multiple AI-generated paths, and trace your thinking over time.

---

## 🚀 Features

- 🌳 **Branching Conversations**  
  Fork from any message to explore alternative replies and ideas.

- 🧠 **Contextual Memory**  
  Maintain and visualize the full history of your conversation tree.

- 📈 **Interactive Tree View**  
  Explore your dialogue visually using a dynamic tree interface.

- 🔍 **Prompt Recall & Navigation**  
  Jump to any previous message and resume from there.

- 📥 **Save & Export**  
  Save your conversation trees and export them as JSON or Markdown.

---

## 🖼️ Demo

> [Insert screenshot or GIF here of branching interface + chat]

---

## 🛠️ Tech Stack

- [x] **Python**
- [x] **Streamlit** – UI layer
- [x] **OpenAI API** (or any LLM backend)
- [x] **NetworkX + PyVis** or **Graphviz** – for tree visualization
- [x] **JSON/SQLite** – for conversation state storage

---

## 📦 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/echotrace.git
cd echotrace

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```
