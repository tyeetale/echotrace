import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os

from tree_manager import NodeManager
from chat_engine import ChatEngine

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chat = ChatEngine(api_key=OPENAI_API_KEY)
tree = NodeManager(storage_path="data/conversations.json")

AVAILABLE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
]
# Set default model in session state
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4"

cols = st.sidebar.columns([2, 1])
with cols[0]:
    model_choice = st.selectbox("Model", AVAILABLE_MODELS, key="openai_model", label_visibility="collapsed")
with cols[1]:
    if st.button("➕", help="Create new chat"):        
        # Create NEW Root node & NEW Branch
        from tree_manager import Node, Branch
        # Create new root node
        root = Node("Start your conversation...", "Hi! How can I help you?")
        tree.nodes[root.id] = root
        # Create new branch
        branch = Branch("main", root.id)
        tree.branches[branch.id] = branch
        tree.current_branch_id = branch.id
        tree.current_node_id = root.id
        tree.save()
        st.session_state.current_branch_id = branch.id
        st.session_state.current_node_id = root.id
        # Optionally clear model pick or keep it
        st.rerun()
        
# --- Guarantee persistent state always has at least one branch and node ---
if not hasattr(tree, "branches") or not tree.branches or not hasattr(tree, "nodes") or not tree.nodes:
    root = tree.nodes[list(tree.nodes.keys())[0]] if tree.nodes else None
    if not root:
        from tree_manager import Node, Branch
        root = Node("Start your conversation...", "Hi! How can I help you?")
        tree.nodes[root.id] = root
    if not tree.branches:
        from tree_manager import Branch
        branch = Branch("main", root.id)
        tree.branches[branch.id] = branch
        tree.current_branch_id = branch.id
    if not tree.current_node_id:
        tree.current_node_id = root.id
    tree.save()

if "current_branch_id" not in st.session_state or st.session_state.current_branch_id not in tree.branches:
    st.session_state.current_branch_id = tree.current_branch_id or list(tree.branches.keys())[0]
    tree.current_branch_id = st.session_state.current_branch_id

if "current_node_id" not in st.session_state or st.session_state.current_node_id not in tree.nodes:
    last_nid = tree.branches[tree.current_branch_id].node_ids[-1]
    st.session_state.current_node_id = last_nid
    tree.current_node_id = last_nid

# Always sync NodeManager's state from the session
tree.current_branch_id = st.session_state.current_branch_id
tree.current_node_id = st.session_state.current_node_id

# --- App UI & chat ---
timeline_nodes = tree.get_branch_timeline_nodes()  # In order, for current branch

st.set_page_config(page_title="EchoTrace", layout="wide")
st.markdown(
    """<h1 style='display:flex;align-items:center;gap:1em;'>
    <span style='font-size:2em;'>🌿</span> <span>EchoTrace</span>
    </h1>
    <div style='font-size:1.1em;color:gray;margin-bottom:1.5em;'>
        Branchable AI chat system — explore multiple threads of thought.
    </div>
    """, unsafe_allow_html=True
)

for node in timeline_nodes:
    if node.user_msg:
        with st.chat_message("user"):
            st.markdown(node.user_msg)
    if node.ai_msg:
        with st.chat_message("assistant"):
            st.markdown(node.ai_msg)

if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Thinking..."):
        # Prepare messages for the AI: full conversation so far, then new user prompt
        messages = []
        for node in timeline_nodes:
            if node.user_msg:
                messages.append({'role': 'user', 'content': node.user_msg})
            if node.ai_msg:
                messages.append({'role': 'assistant', 'content': node.ai_msg})
        messages.append({'role': 'user', 'content': prompt})
        response = chat.get_response(messages)
    with st.chat_message("assistant"):
        st.markdown(response)
    new_node = tree.add_node(prompt, response, parent_id=tree.current_node_id)
    st.session_state.current_node_id = tree.current_node_id
    st.rerun()

# --- SIDEBAR ---
st.sidebar.markdown(
    "<div style='font-weight:700;font-size:1.3em;margin-bottom:.8em;'>Conversations</div>",
    unsafe_allow_html=True
)

    # --- Branch Selector ---
branch_names = {b.id: b.name for b in tree.branches.values()}
options_list = list(branch_names.keys())
cur_idx = options_list.index(tree.current_branch_id)

# Only show a dropdown if >1 branch, else static label
if len(options_list) > 1:
    branch_selector = st.sidebar.selectbox(
        "Branch:",
        options=options_list,
        format_func=lambda bid: branch_names[bid],
        index=cur_idx
    )
    if branch_selector != tree.current_branch_id:
        # Switch branch: jump to last node in that branch
        tree.current_branch_id = branch_selector
        st.session_state.current_branch_id = branch_selector
        last_nid = tree.branches[branch_selector].node_ids[-1]
        tree.current_node_id = last_nid
        st.session_state.current_node_id = last_nid
        st.rerun()
else:
    st.sidebar.markdown(
        f'<div><b>Branch: {branch_names[tree.current_branch_id]}</b></div>',
        unsafe_allow_html=True
    )

st.sidebar.markdown(
    "<div style='color:#bbb;margin-bottom:1.1em;'>Branch = a threaded chat (forks from others). Branches and their history persist.</div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("<b>Timeline:</b>", unsafe_allow_html=True)
timeline_nodes = tree.get_branch_timeline_nodes()

for idx, node in enumerate(timeline_nodes):
    msg_time = datetime.fromisoformat(node.timestamp).strftime("%H:%M")
    preview = (node.user_msg or '')[:20].replace('\n', ' ')
    is_tip = (node.id == timeline_nodes[-1].id)

    txt = f"<span style='color:#aaa;'>{msg_time}</span> — <b>{preview}</b>"
    cols = st.sidebar.columns([5,1]) if not is_tip else [st.sidebar, None]
    with cols[0]:
        st.markdown(txt, unsafe_allow_html=True)
    if not is_tip:
        with cols[1]:
            if st.button("🌱", key=f"branchbtn_{node.id}", help="Branch from here"):
                st.session_state["branching_node"] = node.id

# If a branch button has been clicked, show the input below the timeline
if "branching_node" in st.session_state and st.session_state["branching_node"]:
    node_id = st.session_state["branching_node"]
    branch_name = st.sidebar.text_input("New branch name", key="new_branch_name")
    colA, colB = st.sidebar.columns([1, 1])
    branch_create_clicked = colA.button("Create branch", key="create_branch_btn")
    branch_cancel_clicked = colB.button("Cancel", key="cancel_branch_btn")
    
    if branch_create_clicked:
        final_name = branch_name.strip() or "Branch"
        tree.create_branch_from(final_name, node_id)
        st.session_state.current_branch_id = tree.current_branch_id
        st.session_state.current_node_id = tree.current_node_id
        # CLEAR: Remove the branching_node, let text_input clear on next run
        del st.session_state["branching_node"]
        if "new_branch_name" in st.session_state:
            del st.session_state["new_branch_name"]
        st.rerun()
    elif branch_cancel_clicked:
        del st.session_state["branching_node"]
        if "new_branch_name" in st.session_state:
            del st.session_state["new_branch_name"]
        st.rerun()