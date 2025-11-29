<template>
  <div class="conversation-tree">
    <div class="tree-toolbar">
      <q-btn
        flat
        dense
        icon="zoom_in"
        @click="zoomIn"
        size="sm"
      />
      <q-btn
        flat
        dense
        icon="zoom_out"
        @click="zoomOut"
        size="sm"
      />
      <q-btn
        flat
        dense
        icon="fit_screen"
        @click="fitView"
        size="sm"
      />
      <q-space />
      <q-btn
        flat
        dense
        :icon="isFullscreen ? 'fullscreen_exit' : 'fullscreen'"
        @click="toggleFullscreen"
        size="sm"
      />
    </div>

    <div class="tree-container" :class="{ fullscreen: isFullscreen }">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        v-model:viewport="viewport"
        @node-click="onNodeClick"
        @edge-click="onEdgeClick"
        @node-drag-stop="onNodeDragStop"
        @connect="onConnect"
        :connection-mode="ConnectionMode.Loose"
        :default-edge-options="defaultEdgeOptions"
        :fit-view-on-init="true"
        class="vue-flow-container"
      >
        <Background />
        <Controls />
        <MiniMap />
        
        <!-- Custom Node Types -->
        <template #node-message="{ data }">
          <div class="custom-node message-node" :class="{ current: data.is_current }">
            <div class="node-content">
              <div v-if="data.user_msg" class="user-message">
                {{ data.user_msg }}
              </div>
              <div v-if="data.ai_msg" class="ai-message">
                {{ data.ai_msg }}
              </div>
              <div class="node-timestamp">
                {{ formatTime(data.timestamp) }}
              </div>
            </div>
            <div v-if="data.is_branch_point" class="branch-indicator">
              <q-icon name="account_tree" size="xs" />
            </div>
          </div>
        </template>

        <template #node-branch="{ data }">
          <div class="custom-node branch-node">
            <div class="branch-content">
              <q-icon name="account_tree" size="sm" />
              <span>{{ data.branch_name }}</span>
            </div>
          </div>
        </template>
      </VueFlow>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import {
  VueFlow,
  Background,
  Controls,
  MiniMap,
  ConnectionMode,
  type Node,
  type Edge,
  type Viewport
} from '@vue-flow/core'
import { useConversationStore } from '../stores/conversationStore'
import { useUIStore } from '../stores/uiStore'
import { date } from 'quasar'
import type { ConversationNode, ConversationEdge } from '../types/vue-flow'

const conversationStore = useConversationStore()
const uiStore = useUIStore()

const {
  currentBranchNodes,
  nodes: storeNodes,
  branches,
  currentNode,
  createBranch,
  navigateToNode
} = conversationStore

const { isTreeViewFullscreen: isFullscreen, setTreeViewMode } = uiStore

// Vue Flow state
const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])
const viewport = ref<Viewport>({ x: 0, y: 0, zoom: 1 })

const defaultEdgeOptions = {
  type: 'default',
  animated: true
}

const formatTime = (timestamp: string) => {
  return date.formatDate(timestamp, 'HH:mm')
}

// Convert conversation data to Vue Flow nodes and edges
const convertToFlowData = () => {
  const flowNodes: Node[] = []
  const flowEdges: Edge[] = []

  // Create nodes for each message
  storeNodes.forEach((node, index) => {
    const isCurrent = currentNode?.id === node.id
    const isBranchPoint = branches.some(branch => 
      branch.root_node_id === node.id && branch.id !== conversationStore.currentBranch?.id
    )

    flowNodes.push({
      id: node.id,
      type: 'message',
      position: { x: index * 300, y: 0 },
      data: {
        user_msg: node.user_msg,
        ai_msg: node.ai_msg,
        timestamp: node.timestamp,
        is_current: isCurrent,
        is_branch_point: isBranchPoint
      }
    })
  })

  // Create edges between consecutive nodes in current branch
  const currentBranchNodeIds = conversationStore.currentBranch?.node_ids || []
  for (let i = 0; i < currentBranchNodeIds.length - 1; i++) {
    const sourceId = currentBranchNodeIds[i]
    const targetId = currentBranchNodeIds[i + 1]
    
    flowEdges.push({
      id: `${sourceId}-${targetId}`,
      source: sourceId,
      target: targetId,
      type: 'default'
    })
  }

  // Add branch nodes and edges
  branches.forEach((branch, index) => {
    if (branch.id !== conversationStore.currentBranch?.id) {
      const rootNode = storeNodes.find(n => n.id === branch.root_node_id)
      if (rootNode) {
        const branchNodeId = `branch-${branch.id}`
        
        flowNodes.push({
          id: branchNodeId,
          type: 'branch',
          position: { x: rootNode.position?.x || 0, y: (index + 1) * 150 },
          data: {
            branch_name: branch.name
          }
        })

        flowEdges.push({
          id: `${branch.root_node_id}-${branchNodeId}`,
          source: branch.root_node_id,
          target: branchNodeId,
          type: 'branch'
        })
      }
    }
  })

  nodes.value = flowNodes
  edges.value = flowEdges
}

// Event handlers
const onNodeClick = (event: any) => {
  const nodeId = event.node.id
  if (nodeId.startsWith('branch-')) {
    const branchId = nodeId.replace('branch-', '')
    conversationStore.switchBranch(branchId)
  } else {
    navigateToNode(nodeId)
  }
}

const onEdgeClick = (event: any) => {
  console.log('Edge clicked:', event.edge)
}

const onNodeDragStop = (event: any) => {
  console.log('Node drag stopped:', event.node)
}

const onConnect = (connection: any) => {
  console.log('Connection created:', connection)
}

// Zoom controls
const zoomIn = () => {
  viewport.value.zoom = Math.min(viewport.value.zoom * 1.2, 2)
}

const zoomOut = () => {
  viewport.value.zoom = Math.max(viewport.value.zoom / 1.2, 0.1)
}

const fitView = () => {
  // Vue Flow will handle this automatically
  nextTick(() => {
    // Trigger fit view
  })
}

const toggleFullscreen = () => {
  setTreeViewMode(isFullscreen.value ? 'sidebar' : 'fullscreen')
}

// Watch for changes in conversation data
watch([storeNodes, branches, currentNode], () => {
  convertToFlowData()
}, { deep: true })

onMounted(() => {
  convertToFlowData()
})
</script>

<style scoped>
.conversation-tree {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tree-toolbar {
  display: flex;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #e0e0e0;
  background-color: white;
}

.tree-container {
  flex: 1;
  position: relative;
}

.tree-container.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  background-color: white;
}

.vue-flow-container {
  width: 100%;
  height: 100%;
}

.custom-node {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 8px;
  min-width: 200px;
  max-width: 300px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.custom-node.current {
  border-color: #1976d2;
  box-shadow: 0 4px 8px rgba(25, 118, 210, 0.3);
}

.message-node .node-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-message {
  background-color: #e3f2fd;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.ai-message {
  background-color: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.node-timestamp {
  font-size: 0.75rem;
  color: #666;
  text-align: right;
}

.branch-indicator {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #ff9800;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.branch-node .branch-content {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #1976d2;
}
</style>