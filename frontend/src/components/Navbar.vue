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
              <button @click="handleLogout" class="btn btn-outline-danger">
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
import { useAuth0Store } from '../stores/auth0'
import { useAuth0 } from '@auth0/auth0-vue'

const authStore = useAuthStore()
const auth0Store = useAuth0Store()
const auth0 = useAuth0()
const router = useRouter()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const isAdvertiser = computed(() => authStore.isAdvertiser)
const user = computed(() => authStore.user)

// Sprawdź, czy użytkownik jest zalogowany przez Auth0
const isAuth0User = computed(() => !!authStore.user?.auth0_id)

const handleLogout = async () => {
  // Jeśli użytkownik jest zalogowany przez Auth0, użyj Auth0 do wylogowania
  if (isAuth0User.value && auth0.isAuthenticated.value) {
    await auth0Store.logout()
  } else {
    // W przeciwnym razie użyj standardowego wylogowania
    authStore.logout()
  }
  router.push('/')
}
</script>