<template>
  <div class="conversation-page">
    <!-- Main Chat Area -->
    <div class="main-content" :class="{ 'with-sidebar': !uiStore.isTreeViewFullscreen }">
      <ChatInterface v-if="conversationStore.currentConversation" />
      
      <!-- Empty State -->
      <div v-else class="empty-state">
        <q-icon name="chat" size="4rem" color="grey-5" />
        <div class="text-h6 text-grey-6 q-mt-md">No conversation selected</div>
        <div class="text-body2 text-grey-5 q-mt-sm">
          Select a conversation from the sidebar or create a new one
        </div>
      </div>
    </div>

    <!-- Tree View Sidebar -->
    <q-drawer
      v-if="uiStore.isTreeViewSidebar"
      v-model="uiStore.leftDrawerOpen"
      show-if-above
      bordered
      :width="400"
      :breakpoint="700"
      side="right"
    >
      <ConversationTree />
    </q-drawer>

    <!-- Fullscreen Tree View -->
    <ConversationTree v-if="uiStore.isTreeViewFullscreen" />

    <!-- Branch Management Panel -->
    <q-drawer
      v-model="uiStore.rightDrawerOpen"
      show-if-above
      bordered
      :width="300"
      side="right"
    >
      <BranchManager />
    </q-drawer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useConversationStore } from '../stores/conversationStore'
import { useUIStore } from '../stores/uiStore'
import ChatInterface from '../components/ChatInterface.vue'
import ConversationTree from '../components/ConversationTree.vue'
import BranchManager from '../components/BranchManager.vue'

const conversationStore = useConversationStore()
const uiStore = useUIStore()

onMounted(() => {
  // Load conversations on page mount
  conversationStore.loadConversations()
})
</script>

<style scoped>
.conversation-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-content.with-sidebar {
  margin-right: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 2rem;
}
</style>