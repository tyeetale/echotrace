<template>
  <q-scroll-area class="fit">
    <div class="q-pa-md">
      <div class="row items-center q-mb-md">
        <q-icon name="chat" size="sm" class="q-mr-sm" />
        <span class="text-h6">Conversations</span>
        <q-space />
        <q-btn
          flat
          round
          dense
          icon="add"
          @click="createNewConversation"
          :loading="loading"
        />
      </div>

      <q-list separator>
        <q-item
          v-for="conversation in conversations"
          :key="conversation.id"
          clickable
          v-ripple
          :active="currentConversation?.id === conversation.id"
          @click="loadConversation(conversation.id)"
          class="q-mb-xs"
        >
          <q-item-section>
            <q-item-label>{{ conversation.title }}</q-item-label>
            <q-item-label caption>
              {{ formatDate(conversation.updated_at) }}
            </q-item-label>
          </q-item-section>
          
          <q-item-section side>
            <q-btn
              flat
              round
              dense
              icon="delete"
              size="sm"
              @click.stop="deleteConversation(conversation.id)"
              color="negative"
            />
          </q-item-section>
        </q-item>
      </q-list>

      <q-dialog v-model="showCreateDialog">
        <q-card style="min-width: 300px">
          <q-card-section>
            <div class="text-h6">New Conversation</div>
          </q-card-section>

          <q-card-section>
            <q-input
              v-model="newConversationTitle"
              label="Conversation Title"
              outlined
              :rules="[val => !!val || 'Title is required']"
              ref="titleInput"
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancel" @click="showCreateDialog = false" />
            <q-btn
              color="primary"
              label="Create"
              @click="handleCreateConversation"
              :loading="loading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConversationStore } from '../stores/conversationStore'
import { date } from 'quasar'

const conversationStore = useConversationStore()

const {
  conversations,
  currentConversation,
  loading,
  loadConversations,
  loadConversation,
  createConversation
} = conversationStore

const showCreateDialog = ref(false)
const newConversationTitle = ref('')
const titleInput = ref()

const formatDate = (dateString: string) => {
  return date.formatDate(dateString, 'MMM D, YYYY')
}

const createNewConversation = () => {
  newConversationTitle.value = ''
  showCreateDialog.value = true
  setTimeout(() => {
    titleInput.value?.focus()
  }, 100)
}

const handleCreateConversation = async () => {
  if (!newConversationTitle.value.trim()) return
  
  try {
    await createConversation(newConversationTitle.value.trim())
    showCreateDialog.value = false
  } catch (error) {
    console.error('Failed to create conversation:', error)
  }
}

const deleteConversation = async (id: string) => {
  // TODO: Implement delete functionality
  console.log('Delete conversation:', id)
}

onMounted(() => {
  loadConversations()
})
</script>