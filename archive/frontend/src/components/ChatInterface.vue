<template>
  <div class="chat-interface">
    <!-- Chat Messages -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="node in currentBranchNodes"
        :key="node.id"
        class="message-group"
      >
        <!-- User Message -->
        <div v-if="node.user_msg" class="message user-message">
          <div class="message-content">
            <div class="message-text">{{ node.user_msg }}</div>
            <div class="message-time">
              {{ formatTime(node.timestamp) }}
            </div>
          </div>
        </div>

        <!-- AI Message -->
        <div v-if="node.ai_msg" class="message ai-message">
          <div class="message-content">
            <div class="message-text">{{ node.ai_msg }}</div>
            <div class="message-time">
              {{ formatTime(node.timestamp) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Loading indicator -->
      <div v-if="loading" class="message ai-message">
        <div class="message-content">
          <q-spinner-dots size="sm" class="q-mr-sm" />
          <span>Thinking...</span>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="message-input-container">
      <q-input
        v-model="messageInput"
        placeholder="Type your message..."
        outlined
        dense
        @keyup.enter="sendMessage"
        :loading="loading"
        :disable="loading"
        ref="messageInputRef"
      >
        <template v-slot:append>
          <q-btn
            flat
            round
            dense
            icon="send"
            @click="sendMessage"
            :disable="!messageInput.trim() || loading"
            color="primary"
          />
        </template>
      </q-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue'
import { useConversationStore } from '../stores/conversationStore'
import { date } from 'quasar'

const conversationStore = useConversationStore()

const {
  currentBranchNodes,
  loading,
  addMessage
} = conversationStore

const messageInput = ref('')
const messageInputRef = ref()
const messagesContainer = ref()

const formatTime = (timestamp: string) => {
  return date.formatDate(timestamp, 'HH:mm')
}

const sendMessage = async () => {
  const message = messageInput.value.trim()
  if (!message || loading.value) return

  try {
    messageInput.value = ''
    await addMessage(message)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
    // Restore the message if sending failed
    messageInput.value = message
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Auto-scroll when new messages are added
watch(currentBranchNodes, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })

// Focus input when component mounts
nextTick(() => {
  messageInputRef.value?.focus()
})
</script>

<style scoped>
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message {
  max-width: 80%;
  word-wrap: break-word;
}

.user-message {
  align-self: flex-end;
}

.ai-message {
  align-self: flex-start;
}

.message-content {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
}

.user-message .message-content {
  background-color: #1976d2;
  color: white;
}

.ai-message .message-content {
  background-color: #f5f5f5;
  color: #333;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 4px;
}

.message-input-container {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  background-color: white;
}
</style>