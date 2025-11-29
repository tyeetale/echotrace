export interface Node {
  id: string
  user_msg: string | null
  ai_msg: string | null
  parent_id: string | null
  annotations: string
  timestamp: string
  created_at: string
  updated_at: string
}

export interface Branch {
  id: string
  name: string
  conversation_id: string
  root_node_id: string
  node_ids: string[]
  created_at: string
  updated_at: string
}

export interface Conversation {
  id: string
  title: string
  created_at: string
  updated_at: string
  current_branch_id: string | null
  current_node_id: string | null
}

export interface CreateConversationRequest {
  title: string
}

export interface CreateBranchRequest {
  name: string
  from_node_id: string
}

export interface AddMessageRequest {
  user_msg: string
  parent_id: string
}

export interface AIResponseRequest {
  messages: Array<{
    role: 'user' | 'assistant'
    content: string
  }>
  model?: string
}

export interface AIResponse {
  content: string
  model: string
}

export interface ConversationTree {
  conversation: Conversation
  branches: Branch[]
  nodes: Node[]
  current_branch: Branch | null
  current_node: Node | null
}