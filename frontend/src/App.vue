<template>
  <div id="q-app">
    <q-layout view="lHh Lpr lFf">
      <q-header elevated>
        <q-toolbar>
          <q-toolbar-title>
            <div class="row items-center">
              <q-icon name="account_tree" size="md" class="q-mr-sm" />
              EchoTrace
            </div>
          </q-toolbar-title>
          <q-space />
          <q-btn
            flat
            round
            dense
            :icon="darkMode ? 'light_mode' : 'dark_mode'"
            @click="toggleDarkMode"
          />
        </q-toolbar>
      </q-header>

      <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        bordered
        :width="300"
        :breakpoint="700"
      >
        <SessionManager />
      </q-drawer>

      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import SessionManager from './components/SessionManager.vue'

const $q = useQuasar()
const leftDrawerOpen = ref(true)

const darkMode = computed(() => $q.dark.isActive)

const toggleDarkMode = () => {
  $q.dark.toggle()
}
</script>