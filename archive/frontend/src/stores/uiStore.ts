import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // State
  const leftDrawerOpen = ref(true)
  const rightDrawerOpen = ref(false)
  const treeViewMode = ref<'sidebar' | 'fullscreen'>('sidebar')
  const selectedNodeId = ref<string | null>(null)
  const searchQuery = ref('')
  const showBranchComparison = ref(false)
  const comparisonBranches = ref<{ left: string | null; right: string | null }>({
    left: null,
    right: null
  })

  // Getters
  const isTreeViewFullscreen = computed(() => treeViewMode.value === 'fullscreen')
  const isTreeViewSidebar = computed(() => treeViewMode.value === 'sidebar')

  // Actions
  const toggleLeftDrawer = () => {
    leftDrawerOpen.value = !leftDrawerOpen.value
  }

  const toggleRightDrawer = () => {
    rightDrawerOpen.value = !rightDrawerOpen.value
  }

  const setTreeViewMode = (mode: 'sidebar' | 'fullscreen') => {
    treeViewMode.value = mode
  }

  const selectNode = (nodeId: string | null) => {
    selectedNodeId.value = nodeId
  }

  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }

  const toggleBranchComparison = () => {
    showBranchComparison.value = !showBranchComparison.value
  }

  const setComparisonBranches = (left: string | null, right: string | null) => {
    comparisonBranches.value = { left, right }
  }

  return {
    // State
    leftDrawerOpen,
    rightDrawerOpen,
    treeViewMode,
    selectedNodeId,
    searchQuery,
    showBranchComparison,
    comparisonBranches,
    
    // Getters
    isTreeViewFullscreen,
    isTreeViewSidebar,
    
    // Actions
    toggleLeftDrawer,
    toggleRightDrawer,
    setTreeViewMode,
    selectNode,
    setSearchQuery,
    toggleBranchComparison,
    setComparisonBranches
  }
})