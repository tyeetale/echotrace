import { apiClient } from './api'
import type {
  Conversation,
  ConversationTree,
  CreateConversationRequest,
  CreateBranchRequest,
  AddMessageRequest,
  AIResponseRequest,
  AIResponse
} from '../types/conversation'

export const conversationService = {
  async getConversations(): Promise<Conversation[]> {
    return apiClient.get<Conversation[]>('/conversations')
  },

  async getConversation(id: string): Promise<Conversation> {
    return apiClient.get<Conversation>(`/conversations/${id}`)
  },

  async getConversationTree(id: string): Promise<ConversationTree> {
    return apiClient.get<ConversationTree>(`/conversations/${id}/tree`)
  },

  async createConversation(data: CreateConversationRequest): Promise<Conversation> {
    return apiClient.post<Conversation>('/conversations', data)
  },

  async updateConversation(id: string, data: Partial<Conversation>): Promise<Conversation> {
    return apiClient.put<Conversation>(`/conversations/${id}`, data)
  },

  async deleteConversation(id: string): Promise<void> {
    return apiClient.delete<void>(`/conversations/${id}`)
  },

  async createBranch(conversationId: string, data: CreateBranchRequest): Promise<any> {
    return apiClient.post(`/conversations/${conversationId}/branches`, data)
  },

  async addMessage(conversationId: string, data: AddMessageRequest): Promise<any> {
    return apiClient.post(`/conversations/${conversationId}/messages`, data)
  },

  async updateNode(conversationId: string, nodeId: string, data: any): Promise<any> {
    return apiClient.put(`/conversations/${conversationId}/nodes/${nodeId}`, data)
  },

  async getAIResponse(data: AIResponseRequest): Promise<AIResponse> {
    return apiClient.post<AIResponse>('/ai/response', data)
  }
}