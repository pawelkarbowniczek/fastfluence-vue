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
import { useAuth0 } from '@auth0/auth0-vue'
import { useAuth0Store } from '../stores/auth0'

const router = useRouter()
const auth0 = useAuth0()
const auth0Store = useAuth0Store()
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    console.log('Auth0 Callback - starting process')

    // Czekaj aż Auth0 zakończy przetwarzanie callback
    let attempts = 0
    const maxAttempts = 100 // 10 sekund maksymalnie

    while (auth0.isLoading.value && attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }

    console.log('Auth0 processing complete:', {
      isAuthenticated: auth0.isAuthenticated.value,
      isLoading: auth0.isLoading.value,
      hasUser: !!auth0.user.value,
      hasError: !!auth0.error.value
    })

    // Sprawdź czy są błędy Auth0
    if (auth0.error.value) {
      throw new Error(`Auth0 Error: ${auth0.error.value.message}`)
    }

    // Sprawdź czy użytkownik jest uwierzytelniony
    if (!auth0.isAuthenticated.value || !auth0.user.value) {
      throw new Error('Uwierzytelnianie Auth0 nie powiodło się')
    }

    // Przetwórz uwierzytelnienie w naszym systemie
    const success = await auth0Store.handleAuth0Authentication()

    if (success) {
      console.log('Auth0 authentication successful, redirecting to dashboard')
      router.push('/dashboard')
    } else {
      throw new Error('Błąd integracji z systemem backend')
    }
  } catch (err: any) {
    console.error('Błąd podczas obsługi callback Auth0:', err)
    error.value = err.message || 'Wystąpił błąd podczas logowania. Spróbuj ponownie.'
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