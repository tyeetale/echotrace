<template>
  <div class="branch-manager">
    <div class="q-pa-md">
      <div class="row items-center q-mb-md">
        <q-icon name="account_tree" size="sm" class="q-mr-sm" />
        <span class="text-h6">Branches</span>
      </div>

      <!-- Current Branch Info -->
      <div v-if="currentBranch" class="current-branch q-mb-md">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-subtitle2">Current Branch</div>
            <div class="text-h6">{{ currentBranch.name }}</div>
            <div class="text-caption text-grey-6">
              {{ currentBranch.node_ids.length }} messages
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Branch List -->
      <q-list separator>
        <q-item
          v-for="branch in branches"
          :key="branch.id"
          clickable
          v-ripple
          :active="currentBranch?.id === branch.id"
          @click="switchBranch(branch.id)"
          class="q-mb-xs"
        >
          <q-item-section>
            <q-item-label>{{ branch.name }}</q-item-label>
            <q-item-label caption>
              {{ branch.node_ids.length }} messages
            </q-item-label>
          </q-item-section>
          
          <q-item-section side>
            <q-icon
              name="check_circle"
              color="positive"
              v-if="currentBranch?.id === branch.id"
            />
          </q-item-section>
        </q-item>
      </q-list>

      <!-- Create Branch Button -->
      <q-btn
        v-if="currentNode"
        color="primary"
        outline
        icon="add"
        label="Create Branch"
        class="full-width q-mt-md"
        @click="showCreateBranchDialog = true"
      />

      <!-- Create Branch Dialog -->
      <q-dialog v-model="showCreateBranchDialog">
        <q-card style="min-width: 300px">
          <q-card-section>
            <div class="text-h6">Create New Branch</div>
            <div class="text-caption text-grey-6">
              Branch from: "{{ currentNode?.user_msg?.substring(0, 50) }}..."
            </div>
          </q-card-section>

          <q-card-section>
            <q-input
              v-model="newBranchName"
              label="Branch Name"
              outlined
              :rules="[val => !!val || 'Branch name is required']"
              ref="branchNameInput"
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancel" @click="showCreateBranchDialog = false" />
            <q-btn
              color="primary"
              label="Create"
              @click="handleCreateBranch"
              :loading="loading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useConversationStore } from '../stores/conversationStore'

const conversationStore = useConversationStore()

const {
  currentBranch,
  branches,
  currentNode,
  loading,
  createBranch
} = conversationStore

const showCreateBranchDialog = ref(false)
const newBranchName = ref('')
const branchNameInput = ref()

const switchBranch = async (branchId: string) => {
  await conversationStore.switchBranch(branchId)
}

const handleCreateBranch = async () => {
  if (!newBranchName.value.trim() || !currentNode.value) return
  
  try {
    await createBranch(newBranchName.value.trim(), currentNode.value.id)
    showCreateBranchDialog.value = false
    newBranchName.value = ''
  } catch (error) {
    console.error('Failed to create branch:', error)
  }
}
</script>

<style scoped>
.branch-manager {
  height: 100%;
}

.current-branch {
  background-color: #f5f5f5;
  border-radius: 8px;
}
</style>