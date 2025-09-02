<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="text-center mb-4">
            <h1 class="display-4 fw-bold mb-3">
              <span class="text-primary">Fast</span><span class="text-success">Fluence</span>
            </h1>
            <p class="fs-5 text-muted">Zaloguj się do swojego konta</p>
          </div>

          <div class="card shadow-lg rounded-4 p-4">
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                  <label for="login-email" class="form-label">Email</label>
                  <input
                    v-model="form.username"
                    type="email"
                    class="form-control"
                    id="login-email"
                    required
                  >
                </div>

                <div class="mb-3">
                  <label for="login-password" class="form-label">Hasło</label>
                  <input
                    v-model="form.password"
                    type="password"
                    class="form-control"
                    id="login-password"
                    required
                  >
                </div>

                <div v-if="error" class="alert alert-danger">
                  {{ error }}

                  <!-- Show resend activation link for unactivated accounts -->
                  <div v-if="showActivationResend" class="mt-2">
                    <hr>
                    <button
                      type="button"
                      @click="resendActivation"
                      class="btn btn-sm btn-outline-primary"
                      :disabled="isResending"
                    >
                      {{ isResending ? 'Wysyłanie...' : 'Wyślij ponownie email aktywacyjny' }}
                    </button>
                  </div>
                </div>

                <div v-if="resendSuccess" class="alert alert-success">
                  Email aktywacyjny został wysłany ponownie. Sprawdź swoją skrzynkę pocztową.
                </div>

                <div class="d-grid gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading"
                  >
                    {{ isLoading ? 'Logowanie...' : 'Zaloguj się' }}
                  </button>

                  <!-- Auth0 login buttons -->
                  <div class="auth0-login-section">
                    <div class="text-center my-3 position-relative">
                      <hr class="text-muted">
                      <span class="position-absolute top-50 start-50 translate-middle px-3 bg-white text-muted">
                        lub
                      </span>
                    </div>

                    <div class="d-grid gap-2 mt-3">
                      <button
                        type="button"
                        @click="loginWithAuth0('advertiser')"
                        class="btn btn-outline-primary"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-sign-in-alt me-2"></i>
                        Zaloguj jako reklamodawca przez Auth0
                      </button>

                      <button
                        type="button"
                        @click="loginWithAuth0('creator')"
                        class="btn btn-outline-success"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-sign-in-alt me-2"></i>
                        Zaloguj jako influencer przez Auth0
                      </button>
                    </div>
                  </div>

                  <div class="text-center mt-3">
                    <span class="text-muted">Nie masz konta? </span>
                    <router-link to="/register" class="text-decoration-none">
                      Zarejestruj się
                    </router-link>
                  </div>

                  <div class="text-center">
                    <router-link to="/" class="text-muted text-decoration-none">
                      ← Powrót do strony głównej
                    </router-link>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAuth0Store } from '../stores/auth0'
import { authApi } from '../services/api'
import type { UserRole } from '../types'

const authStore = useAuthStore()
const auth0Store = useAuth0Store()
const router = useRouter()

const isLoading = ref(false)
const isAuth0Loading = ref(false)
const error = ref<string | null>(null)
const isResending = ref(false)
const resendSuccess = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const showActivationResend = computed(() => {
  return error.value?.includes('nie zostało jeszcze aktywowane')
})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = null
    resendSuccess.value = false

    await authStore.login(form)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd logowania'
  } finally {
    isLoading.value = false
  }
}

const loginWithAuth0 = async (role: UserRole) => {
  try {
    isAuth0Loading.value = true
    error.value = null

    await auth0Store.login(role)
    // Przekierowanie jest obsługiwane przez Auth0
  } catch (err: any) {
    error.value = err.message || 'Błąd logowania przez Auth0'
  } finally {
    isAuth0Loading.value = false
  }
}

const resendActivation = async () => {
  try {
    isResending.value = true
    await authApi.resendActivation(form.username)
    resendSuccess.value = true
    error.value = null
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd wysyłania emaila aktywacyjnego'
  } finally {
    isResending.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(125, 60, 255, 0.1) 0%, rgba(212, 255, 50, 0.1) 100%);
}

.card {
  border: none;
  backdrop-filter: blur(10px);
}

.auth0-login-section hr {
  opacity: 0.25;
}
</style>