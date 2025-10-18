import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Conversation, Node, Branch, ConversationTree } from '../types/conversation'
import { conversationService } from '../services/conversationService'

export const useConversationStore = defineStore('conversation', () => {
  // State
  const conversations = ref<Conversation[]>([])
  const currentConversation = ref<Conversation | null>(null)
  const currentBranch = ref<Branch | null>(null)
  const currentNode = ref<Node | null>(null)
  const nodes = ref<Node[]>([])
  const branches = ref<Branch[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const currentBranchNodes = computed(() => {
    if (!currentBranch.value) return []
    return nodes.value.filter(node => 
      currentBranch.value!.node_ids.includes(node.id)
    ).sort((a, b) => 
      currentBranch.value!.node_ids.indexOf(a.id) - currentBranch.value!.node_ids.indexOf(b.id)
    )
  })

  const currentNodeIndex = computed(() => {
    if (!currentNode.value || !currentBranch.value) return -1
    return currentBranch.value.node_ids.indexOf(currentNode.value.id)
  })

  const canGoBack = computed(() => currentNodeIndex.value > 0)
  const canGoForward = computed(() => 
    currentNodeIndex.value < currentBranchNodes.value.length - 1
  )

  // Actions
  const loadConversations = async () => {
    try {
      loading.value = true
      error.value = null
      const data = await conversationService.getConversations()
      conversations.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load conversations'
    } finally {
      loading.value = false
    }
  }

  const loadConversation = async (conversationId: string) => {
    try {
      loading.value = true
      error.value = null
      const tree = await conversationService.getConversationTree(conversationId)
      
      currentConversation.value = tree.conversation
      currentBranch.value = tree.current_branch
      currentNode.value = tree.current_node
      nodes.value = tree.nodes
      branches.value = tree.branches
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load conversation'
    } finally {
      loading.value = false
    }
  }

  const createConversation = async (title: string) => {
    try {
      loading.value = true
      error.value = null
      const conversation = await conversationService.createConversation(title)
      conversations.value.unshift(conversation)
      await loadConversation(conversation.id)
      return conversation
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create conversation'
      throw err
    } finally {
      loading.value = false
    }
  }

  const addMessage = async (userMsg: string) => {
    if (!currentConversation.value || !currentNode.value) {
      throw new Error('No active conversation or node')
    }

    try {
      loading.value = true
      error.value = null
      
      // Get AI response
      const messages = currentBranchNodes.value.flatMap(node => [
        ...(node.user_msg ? [{ role: 'user' as const, content: node.user_msg }] : []),
        ...(node.ai_msg ? [{ role: 'assistant' as const, content: node.ai_msg }] : [])
      ])
      messages.push({ role: 'user', content: userMsg })

      const aiResponse = await conversationService.getAIResponse(messages)
      
      // Add the new node
      const newNode = await conversationService.addMessage({
        user_msg: userMsg,
        parent_id: currentNode.value.id
      })

      // Update the node with AI response
      const updatedNode = await conversationService.updateNode(newNode.id, {
        ai_msg: aiResponse.content
      })

      // Update local state
      const nodeIndex = nodes.value.findIndex(n => n.id === newNode.id)
      if (nodeIndex >= 0) {
        nodes.value[nodeIndex] = updatedNode
      } else {
        nodes.value.push(updatedNode)
      }

      // Add to current branch
      if (currentBranch.value) {
        currentBranch.value.node_ids.push(updatedNode.id)
        currentNode.value = updatedNode
      }

      return updatedNode
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add message'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createBranch = async (name: string, fromNodeId: string) => {
    if (!currentConversation.value) {
      throw new Error('No active conversation')
    }

    try {
      loading.value = true
      error.value = null
      
      const branch = await conversationService.createBranch({
        name,
        from_node_id: fromNodeId
      })

      branches.value.push(branch)
      currentBranch.value = branch
      currentNode.value = nodes.value.find(n => n.id === fromNodeId) || null

      return branch
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create branch'
      throw err
    } finally {
      loading.value = false
    }
  }

  const switchBranch = async (branchId: string) => {
    const branch = branches.value.find(b => b.id === branchId)
    if (!branch) return

    currentBranch.value = branch
    currentNode.value = nodes.value.find(n => n.id === branch.node_ids[branch.node_ids.length - 1]) || null

    // Update conversation's current branch
    if (currentConversation.value) {
      await conversationService.updateConversation(currentConversation.value.id, {
        current_branch_id: branchId,
        current_node_id: currentNode.value?.id || null
      })
    }
  }

  const navigateToNode = (nodeId: string) => {
    const node = nodes.value.find(n => n.id === nodeId)
    if (node && currentBranch.value?.node_ids.includes(nodeId)) {
      currentNode.value = node
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    conversations,
    currentConversation,
    currentBranch,
    currentNode,
    nodes,
    branches,
    loading,
    error,
    
    // Getters
    currentBranchNodes,
    currentNodeIndex,
    canGoBack,
    canGoForward,
    
    // Actions
    loadConversations,
    loadConversation,
    createConversation,
    addMessage,
    createBranch,
    switchBranch,
    navigateToNode,
    clearError
  }
})