import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, userApi } from '../services/api'
import type { User, LoginData, RegisterData } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdvertiser = computed(() => user.value?.role === 'advertiser')
  const isCreator = computed(() => user.value?.role === 'creator')

  const login = async (loginData: LoginData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await authApi.login(loginData)
      token.value = response.access_token
      localStorage.setItem('access_token', response.access_token)
      
      await fetchCurrentUser()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd logowania'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (registerData: RegisterData) => {
    try {
      isLoading.value = true
      error.value = null
      
      const newUser = await authApi.register(registerData)
      
      // Auto-login after registration
      await login({
        username: registerData.email,
        password: registerData.password
      })
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd rejestracji'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchCurrentUser = async () => {
    try {
      if (!token.value) return
      
      const currentUser = await userApi.getCurrentUser()
      user.value = currentUser
    } catch (err: any) {
      console.error('Error fetching current user:', err)
      logout()
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
  }

  const updateProfile = async (data: Partial<User>) => {
    try {
      const updatedUser = await userApi.updateCurrentUser(data)
      user.value = updatedUser
      return updatedUser
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd aktualizacji profilu'
      throw err
    }
  }

  // Initialize store
  if (token.value) {
    fetchCurrentUser()
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    isAdvertiser,
    isCreator,
    login,
    register,
    logout,
    updateProfile,
    fetchCurrentUser
  }
})