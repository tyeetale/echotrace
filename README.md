# 🌿 EchoTrace - Modern Branchable AI Conversations

**EchoTrace** is a modern, branchable AI conversation system built with Vue.js 3, TypeScript, Quasar, and FastAPI. It allows you to fork conversations at any point, explore multiple AI-generated paths, and trace your thinking over time with an intuitive tree-based interface.

## ✨ Features

- 🌳 **Interactive Tree Visualization** - Drag, zoom, and navigate conversation trees with Vue Flow
- 🧠 **Contextual Memory** - Maintain full conversation history across branches
- 🔀 **Branching Conversations** - Fork from any message to explore alternative paths
- 📱 **Responsive Design** - Mobile-first design with Quasar components
- 🎨 **Modern UI/UX** - Clean, intuitive interface with dark/light themes
- ⚡ **Real-time Updates** - Instant updates with Pinia state management
- 🔍 **Search & Filter** - Find specific messages or branches quickly
- 📤 **Export/Import** - Save conversations in multiple formats
- ⌨️ **Keyboard Shortcuts** - Power user features for efficiency

## 🛠️ Tech Stack

### Frontend
- **Vue.js 3** with Composition API
- **TypeScript** for type safety
- **Quasar Framework** for UI components
- **Vue Flow** for interactive tree visualization
- **Pinia** for state management
- **Vite** for fast development and building

### Backend
- **FastAPI** for high-performance API
- **SQLAlchemy** for database ORM
- **SQLite** for local data storage
- **OpenAI API** for AI responses
- **Pydantic** for data validation

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- OpenAI API key

### Installation

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd echotrace
   ```

2. **Setup backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Setup frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Start both servers**
   ```bash
   # From project root
   ./start.sh
   ```

   Or start manually:
   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   python run.py

   # Terminal 2 - Frontend  
   cd frontend
   npm run dev
   ```

5. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
echotrace/
├── frontend/                 # Vue.js frontend
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── stores/         # Pinia stores
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── app/                # Main application
│   ├── database/           # Database models and setup
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── requirements.txt
└── README.md
```

## 🎯 Core Concepts

### Conversations
- **Conversations** are the top-level containers
- Each conversation has multiple **branches**
- Branches represent different conversation paths
- Only one branch is "active" at a time

### Nodes
- **Nodes** are individual messages in a conversation
- Each node can have a user message, AI response, or both
- Nodes are connected in a tree structure
- You can branch from any node to create alternative paths

### Branching
- Click any message to create a new branch
- Branches inherit the conversation history up to that point
- Switch between branches to explore different paths
- Each branch maintains its own conversation flow

## 🎮 Usage

### Creating Conversations
1. Click the "+" button in the sidebar
2. Enter a conversation title
3. Start chatting with the AI

### Branching
1. Click the tree icon (🌱) next to any message
2. Enter a branch name
3. Continue the conversation from that point

### Navigation
- Use the tree view to see the full conversation structure
- Click nodes to jump to specific messages
- Switch between branches using the branch panel
- Use zoom controls to navigate large trees

### Keyboard Shortcuts
- `Ctrl/Cmd + N` - New conversation
- `Ctrl/Cmd + B` - Create branch from current message
- `Ctrl/Cmd + K` - Focus search
- `Ctrl/Cmd + D` - Toggle dark mode

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run type-check   # Run TypeScript checks
```

### Backend Development
```bash
cd backend
source venv/bin/activate
python run.py        # Start with auto-reload
```

### Database
The app uses SQLite by default. The database file is created automatically at `backend/echotrace.db`.

To reset the database:
```bash
rm backend/echotrace.db
# Restart the backend server
```

## 🚀 Deployment

### Local Production Build
```bash
# Build frontend
cd frontend
npm run build

# Serve with a static file server
npx serve dist
```

### Docker (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Vue.js](https://vuejs.org/)
- UI components by [Quasar](https://quasar.dev/)
- Tree visualization by [Vue Flow](https://vueflow.dev/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- AI responses by [OpenAI](https://openai.com/)

---

**EchoTrace** - Branch your thoughts, explore your ideas. 🌿