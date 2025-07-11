<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
    <div class="container">
      <router-link to="/" class="navbar-brand fw-bold fs-3">
        <span class="text-primary">Fast</span><span class="text-success">Fluence</span>
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link to="/" class="nav-link">Strona główna</router-link>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <router-link to="/dashboard" class="nav-link">Panel</router-link>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <router-link to="/me" class="nav-link">Profil</router-link>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <button @click="logout" class="btn btn-outline-danger ms-2">
              Wyloguj
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isAuthenticated = computed(() => authStore.isAuthenticated)

const logout = () => {
  authStore.logout()
  router.push('/')
}
</script>