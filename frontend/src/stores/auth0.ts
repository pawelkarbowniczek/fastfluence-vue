import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuth0 } from '@auth0/auth0-vue'
import { authApi } from '../services/api'
import { useAuthStore } from './auth'
import type { UserRole } from '../types'

export const useAuth0Store = defineStore('auth0', () => {
  const auth0 = useAuth0()
  const authStore = useAuthStore()

  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => auth0.isAuthenticated.value)

  // Funkcja do zalogowania użytkownika za pomocą Auth0
  const login = async (role: UserRole) => {
    try {
      // Zapisz wybraną rolę do localStorage, aby użyć jej podczas callback
      localStorage.setItem('auth0_selected_role', role)

      // Zaloguj za pomocą Auth0
      await auth0.loginWithRedirect({
        appState: { targetUrl: '/dashboard' }
      })
    } catch (err: any) {
      error.value = err.message || 'Błąd logowania przez Auth0'
      throw err
    }
  }

  // Funkcja do wylogowania użytkownika
  const logout = async () => {
    try {
      // Wyloguj zarówno z Auth0, jak i z naszego systemu
      await auth0.logout({
        logoutParams: {
          returnTo: window.location.origin
        }
      })
      authStore.logout()
    } catch (err: any) {
      console.error('Błąd wylogowania z Auth0:', err)
    }
  }

  // Funkcja do integracji zalogowanego użytkownika Auth0 z naszym systemem
  const handleAuth0Authentication = async () => {
    try {
      if (auth0.isAuthenticated.value && auth0.user.value) {
        isLoading.value = true
        error.value = null

        // Pobierz informacje o użytkowniku z Auth0
        const auth0User = auth0.user.value

        // Pobierz zapisaną rolę z localStorage lub ustaw domyślną
        const selectedRole = localStorage.getItem('auth0_selected_role') as UserRole || 'creator'

        // Wyślij dane użytkownika Auth0 do naszego API
        const response = await authApi.auth0Login({
          auth0_id: auth0User.sub as string,
          email: auth0User.email as string,
          display_name: auth0User.name || auth0User.nickname || '',
          role: selectedRole,
          picture: auth0User.picture || ''
        })

        // Zapisz token JWT z naszego systemu
        authStore.setToken(response.access_token)

        // Pobierz dane użytkownika z naszego systemu
        await authStore.fetchCurrentUser()

        // Wyczyść zapisaną rolę
        localStorage.removeItem('auth0_selected_role')

        return true
      }
      return false
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd integracji z Auth0'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    handleAuth0Authentication
  }
})