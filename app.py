import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os

from chat_engine import ChatEngine
from tree_manager import NodeManager, Node, Branch
from session_manager import SessionManager

# ------------ INIT & CONFIG ---------------
st.set_page_config(page_title="EchoTrace", layout="wide")
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AVAILABLE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
]

####---- SESSION SETUP AND LOADING ----####
sess_mgr = SessionManager()
def load_sessions():
    """Always reload & rebuild session lists"""
    sessions = sess_mgr.list_sessions()
    session_titles = [s["title"] for s in sessions]
    session_files = [str(s["filename"]) for s in sessions]
    return sessions, session_titles, session_files

sessions, session_titles, session_files = load_sessions()

if not session_files:
    # Ensure at least one session exists
    sess_mgr.create_session()
    sessions, session_titles, session_files = load_sessions()

if not session_files:
    st.error("Could not create or find a session file. Check session storage and file permissions.")
    st.stop()


####---- SIDEBAR UI ----####
sidebar_top = st.sidebar.container()

# --- Model dropdown --- #
model_ix = AVAILABLE_MODELS.index("gpt-4") if "gpt-4" in AVAILABLE_MODELS else 0
model = sidebar_top.selectbox(
    "Model",
    AVAILABLE_MODELS,
    index=model_ix,
    key="openai_model"
)
sidebar_top.markdown("**Conversation**")

# --- New conversation button --- #
if sidebar_top.button("➕ Start a new conversation"):
    fn = sess_mgr.create_session()
    sessions, session_titles, session_files = load_sessions()
    cur_idx = session_files.index(str(fn))
    st.session_state["conv_selector_target_idx"] = cur_idx    # <--- for next rerun
    st.session_state["cur_session"] = str(fn)
    for k in ["current_branch_id", "current_node_id"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

# --- Conversation selectbox --- #
selectbox_index = 0
if "conv_selector_target_idx" in st.session_state:
    selectbox_index = st.session_state.pop("conv_selector_target_idx")
elif "cur_session" in st.session_state and st.session_state["cur_session"] in session_files:
    selectbox_index = session_files.index(st.session_state["cur_session"])

conv_idx = sidebar_top.selectbox(
    "",
    options=list(range(len(sessions))),
    format_func=lambda i: session_titles[i],
    index=selectbox_index,
    key="conv_selector"
)
st.session_state["cur_session"] = session_files[conv_idx]

####---- LOAD CURRENT SESSION ----####
tree = NodeManager(storage_path=st.session_state["cur_session"])
chat = ChatEngine(api_key=OPENAI_API_KEY)

# Guarantee 1 branch/node for new conversation
if not tree.branches or not tree.nodes:
    root = Node("default", "Ask a question!")
    tree.nodes[root.id] = root
    main_branch = Branch("main", root.id)
    tree.branches[main_branch.id] = main_branch
    tree.current_branch_id = main_branch.id
    tree.current_node_id = root.id
    tree.save()

# Recalculate branch/node state from file if missing
if "current_branch_id" not in st.session_state or st.session_state.current_branch_id not in tree.branches:
    st.session_state.current_branch_id = tree.current_branch_id
if "current_node_id" not in st.session_state or st.session_state.current_node_id not in tree.nodes:
    last_nid = tree.branches[tree.current_branch_id].node_ids[-1]
    st.session_state.current_node_id = last_nid

tree.current_branch_id = st.session_state.current_branch_id
tree.current_node_id = st.session_state.current_node_id

####---- MAIN APP BODY ----####

st.markdown(
    """<h1 style='display:flex;align-items:center;gap:1em;'>
    <span style='font-size:2em;'>🌿</span> <span>EchoTrace</span>
    </h1>
    <div style='font-size:1.1em;color:gray;margin-bottom:1.5em;'>
        Branchable AI chat system — explore multiple threads of thought. Each conversation is independent.
    </div>
    """,
    unsafe_allow_html=True,
)

timeline_nodes = tree.get_branch_timeline_nodes()
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
        messages = []
        for node in timeline_nodes:
            if node.user_msg:
                messages.append({'role': 'user', 'content': node.user_msg})
            if node.ai_msg:
                messages.append({'role': 'assistant', 'content': node.ai_msg})
        messages.append({'role': 'user', 'content': prompt})
        response = chat.get_response(messages, model=st.session_state.openai_model)
    with st.chat_message("assistant"):
        st.markdown(response)
    new_node = tree.add_node(prompt, response, parent_id=tree.current_node_id)
    st.session_state.current_node_id = tree.current_node_id
    st.rerun()

#### ---- SIDEBAR CONTINUES: BRANCH & TIMELINE ---- ####

st.sidebar.markdown("<b>Branches</b>", unsafe_allow_html=True)
branch_names = {b.id: b.name for b in tree.branches.values()}
options_list = list(branch_names.keys())
cur_idx = options_list.index(tree.current_branch_id)
if len(options_list) > 1:
    branch_selector = st.sidebar.selectbox(
        "Branch:",
        options=options_list,
        format_func=lambda bid: branch_names[bid],
        index=cur_idx
    )
    if branch_selector != tree.current_branch_id:
        tree.current_branch_id = branch_selector
        st.session_state.current_branch_id = branch_selector
        last_nid = tree.branches[branch_selector].node_ids[-1]
        tree.current_node_id = last_nid
        st.session_state.current_node_id = last_nid
        st.rerun()
else:
    st.sidebar.markdown(f'<b>Branch: {branch_names[tree.current_branch_id]}</b>', unsafe_allow_html=True)
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
        del st.session_state["branching_node"]
        if "new_branch_name" in st.session_state:
            del st.session_state["new_branch_name"]
        st.rerun()
    elif branch_cancel_clicked:
        del st.session_state["branching_node"]
        if "new_branch_name" in st.session_state:
            del st.session_state["new_branch_name"]
        st.rerun()