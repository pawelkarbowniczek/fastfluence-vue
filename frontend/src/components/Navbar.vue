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
                <i class="fas fa-home me-1"></i>
                {{ isAdvertiser ? 'Panel' : 'Znajdź zlecenia' }}
              </router-link>
            </li>
            <li v-if="isAdvertiser" class="nav-item">
              <router-link to="/campaigns/add" class="nav-link">
                <i class="fas fa-plus me-1"></i>
                Dodaj kampanię
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/me" class="nav-link">
                <i class="fas fa-user me-1"></i>
                Profil
              </router-link>
            </li>
            <li class="nav-item dropdown" v-if="user">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <span class="fw-semibold">{{ user.display_name }}</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                <li>
                  <router-link class="dropdown-item" to="/me">
                    <i class="fas fa-user-edit me-2"></i>
                    Edytuj profil
                  </router-link>
                </li>
                <li v-if="isAdvertiser">
                  <router-link class="dropdown-item" to="/campaigns/add">
                    <i class="fas fa-plus me-2"></i>
                    Nowa kampania
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <button @click="handleLogout" class="dropdown-item text-danger">
                    <i class="fas fa-sign-out-alt me-2"></i>
                    Wyloguj się
                  </button>
                </li>
              </ul>
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

<style scoped>
.navbar {
  backdrop-filter: blur(10px);
  background: rgba(248, 249, 250, 0.95) !important;
}

.navbar-brand {
  transition: transform 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.05);
}

.nav-link {
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 0.25rem;
  padding: 0.5rem 1rem !important;
}

.nav-link:hover {
  background: rgba(125, 60, 255, 0.1);
  color: var(--violet) !important;
  transform: translateY(-2px);
}

.btn-primary {
  background: var(--violet);
  border-color: var(--violet);
  border-radius: 25px;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #6B2FDB;
  border-color: #6B2FDB;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(125, 60, 255, 0.3);
}

.dropdown-menu {
  border: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  border-radius: 12px;
  padding: 0.5rem 0;
}

.dropdown-item {
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: rgba(125, 60, 255, 0.1);
  color: var(--violet);
}

.dropdown-item.text-danger:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545 !important;
}
</style>