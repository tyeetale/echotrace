import type { Node as VueFlowNode, Edge as VueFlowEdge } from '@vue-flow/core'

export interface ConversationNode extends VueFlowNode {
  id: string
  type: 'message' | 'branch'
  data: {
    user_msg: string | null
    ai_msg: string | null
    timestamp: string
    is_current: boolean
    is_branch_point: boolean
  }
  position: { x: number; y: number }
}

export interface ConversationEdge extends VueFlowEdge {
  id: string
  source: string
  target: string
  type: 'default' | 'branch'
  data?: {
    branch_name?: string
  }
}

export interface FlowViewport {
  x: number
  y: number
  zoom: number
}