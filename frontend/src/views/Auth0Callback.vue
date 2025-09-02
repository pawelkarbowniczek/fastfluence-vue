<template>
  <div class="callback-page">
    <div class="container py-5 text-center">
      <div class="spinner-border text-primary mb-3" role="status">
        <span class="visually-hidden">Ładowanie...</span>
      </div>
      <h2>Logowanie przez Auth0...</h2>
      <p class="text-muted">Proszę czekać, przetwarzamy dane logowania.</p>

      <div v-if="error" class="alert alert-danger mt-4">
        {{ error }}
        <div class="mt-3">
          <router-link to="/login" class="btn btn-outline-primary">
            Powrót do logowania
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth0Store } from '../stores/auth0'

const router = useRouter()
const auth0Store = useAuth0Store()
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    // Poczekaj na zakończenie procesu autoryzacji Auth0
    const success = await auth0Store.handleAuth0Authentication()

    if (success) {
      // Przekieruj do dashboardu
      router.push('/dashboard')
    } else {
      router.push('/login')
    }
  } catch (err: any) {
    console.error('Błąd podczas obsługi callback Auth0:', err)
    error.value = 'Wystąpił błąd podczas logowania. Spróbuj ponownie.'
  }
})
</script>

<style scoped>
.callback-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>