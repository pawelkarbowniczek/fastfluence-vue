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
          <!-- Guest navigation -->
          <template v-if="!isAuthenticated">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Strona główna</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Logowanie</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="btn btn-primary ms-2">
                Rejestracja
              </router-link>
            </li>
          </template>

          <!-- Authenticated navigation -->
          <template v-else>
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">
                {{ isAdvertiser ? 'Panel' : 'Znajdź zlecenie' }}
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/me" class="nav-link">Profil</router-link>
            </li>
            <li class="nav-item">
              <span class="navbar-text me-2">{{ user?.display_name }}</span>
            </li>
            <li class="nav-item">
              <button @click="logout" class="btn btn-outline-danger">
                Wyloguj
              </button>
            </li>
          </template>
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
const isAdvertiser = computed(() => authStore.isAdvertiser)
const user = computed(() => authStore.user)

const logout = () => {
  authStore.logout()
  router.push('/')
}
</script>