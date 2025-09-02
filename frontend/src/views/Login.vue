<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <!-- Logo Section -->
          <div class="text-center mb-4">
            <div class="logo-section">
              <div class="logo-circle mb-3">
                <i class="fas fa-sign-in-alt fa-2x"></i>
              </div>
              <h1 class="display-4 fw-bold mb-3 text-white">
                <span style="color: var(--violet);">Fast</span><span style="color: var(--lime);">Fluence</span>
              </h1>
              <p class="fs-5 text-white opacity-75">Zaloguj się do swojego konta</p>
            </div>
          </div>

          <!-- Login Card -->
          <div class="login-card">
            <div class="card-header-gradient text-white text-center">
              <h3 class="mb-0 fw-bold">Logowanie</h3>
              <p class="mb-0 opacity-75">Wprowadź swoje dane dostępowe</p>
            </div>

            <div class="card-body-white">
              <form @submit.prevent="handleSubmit">
                <div class="mb-4">
                  <label for="login-email" class="form-label fw-semibold">
                    <i class="fas fa-envelope me-2 text-primary"></i>
                    Email
                  </label>
                  <input
                    v-model="form.username"
                    type="email"
                    class="form-control form-control-custom"
                    id="login-email"
                    placeholder="Wprowadź swój adres email"
                    required
                  >
                </div>

                <div class="mb-4">
                  <label for="login-password" class="form-label fw-semibold">
                    <i class="fas fa-lock me-2 text-primary"></i>
                    Hasło
                  </label>
                  <input
                    v-model="form.password"
                    type="password"
                    class="form-control form-control-custom"
                    id="login-password"
                    placeholder="Wprowadź swoje hasło"
                    required
                  >
                </div>

                <div v-if="error" class="alert alert-danger alert-custom">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ error }}

                  <!-- Show resend activation link for unactivated accounts -->
                  <div v-if="showActivationResend" class="mt-3">
                    <hr class="opacity-25">
                    <button
                      type="button"
                      @click="resendActivation"
                      class="btn btn-sm btn-outline-primary"
                      :disabled="isResending"
                    >
                      <i class="fas fa-paper-plane me-2"></i>
                      {{ isResending ? 'Wysyłanie...' : 'Wyślij ponownie email aktywacyjny' }}
                    </button>
                  </div>
                </div>

                <div v-if="resendSuccess" class="alert alert-success alert-custom">
                  <i class="fas fa-check-circle me-2"></i>
                  Email aktywacyjny został wysłany ponownie. Sprawdź swoją skrzynkę pocztową.
                </div>

                <div class="d-grid gap-3">
                  <button
                    type="submit"
                    class="btn btn-primary-gradient btn-lg"
                    :disabled="isLoading"
                  >
                    <i class="fas fa-sign-in-alt me-2"></i>
                    {{ isLoading ? 'Logowanie...' : 'Zaloguj się' }}
                  </button>

                  <!-- Auth0 login buttons -->
                  <div class="auth0-section">
                    <div class="divider-custom">
                      <span class="divider-text">lub kontynuuj z</span>
                    </div>

                    <div class="d-grid gap-2 mt-3">
                      <button
                        type="button"
                        @click="loginWithAuth0('advertiser')"
                        class="btn btn-auth0-advertiser"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-bullhorn me-2"></i>
                        Zaloguj jako reklamodawca
                      </button>

                      <button
                        type="button"
                        @click="loginWithAuth0('creator')"
                        class="btn btn-auth0-creator"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-star me-2"></i>
                        Zaloguj jako influencer
                      </button>
                    </div>
                  </div>

                  <!-- Footer Links -->
                  <div class="text-center mt-4">
                    <div class="link-section">
                      <span class="text-muted">Nie masz konta? </span>
                      <router-link to="/register" class="link-custom">
                        <i class="fas fa-user-plus me-1"></i>
                        Zarejestruj się
                      </router-link>
                    </div>

                    <div class="link-section mt-2">
                      <router-link to="/" class="link-back">
                        <i class="fas fa-arrow-left me-2"></i>
                        Powrót do strony głównej
                      </router-link>
                    </div>
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.logo-section {
  margin-bottom: 2rem;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: white;
  backdrop-filter: blur(10px);
  margin: 0 auto;
}

.login-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.card-header-gradient {
  background: linear-gradient(135deg, var(--violet) 0%, #6B2FDB 100%);
  padding: 2rem;
  border-bottom: none;
}

.card-body-white {
  background: white;
  padding: 2.5rem;
}

.form-control-custom {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-control-custom:focus {
  border-color: var(--violet);
  box-shadow: 0 0 0 0.2rem rgba(125, 60, 255, 0.15);
  background: white;
}

.form-label {
  color: #495057;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.btn-primary-gradient {
  background: linear-gradient(135deg, var(--violet) 0%, #6B2FDB 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 1rem 2rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-size: 1.1rem;
}

.btn-primary-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(125, 60, 255, 0.4);
  color: white;
}

.btn-primary-gradient:disabled {
  opacity: 0.7;
  transform: none;
}

.auth0-section {
  margin-top: 1.5rem;
}

.divider-custom {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.divider-custom::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #dee2e6, transparent);
}

.divider-text {
  background: white;
  padding: 0 1rem;
  color: #6c757d;
  font-size: 0.875rem;
  font-weight: 500;
}

.btn-auth0-advertiser {
  background: rgba(125, 60, 255, 0.1);
  border: 2px solid rgba(125, 60, 255, 0.2);
  color: var(--violet);
  font-weight: 600;
  padding: 0.875rem 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-auth0-advertiser:hover {
  background: rgba(125, 60, 255, 0.2);
  border-color: var(--violet);
  color: var(--violet);
  transform: translateY(-1px);
}

.btn-auth0-creator {
  background: rgba(212, 255, 50, 0.1);
  border: 2px solid rgba(212, 255, 50, 0.3);
  color: #5a6c2d;
  font-weight: 600;
  padding: 0.875rem 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-auth0-creator:hover {
  background: rgba(212, 255, 50, 0.2);
  border-color: var(--lime);
  color: #4a5a23;
  transform: translateY(-1px);
}

.alert-custom {
  border: none;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
}

.alert-danger {
  background: rgba(220, 53, 69, 0.1);
  color: #842029;
  border-left: 4px solid #dc3545;
}

.alert-success {
  background: rgba(25, 135, 84, 0.1);
  color: #0a3622;
  border-left: 4px solid #198754;
}

.link-section {
  padding: 0.5rem 0;
}

.link-custom {
  color: var(--violet);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.link-custom:hover {
  color: #6B2FDB;
  text-decoration: underline;
}

.link-back {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.link-back:hover {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .login-page {
    padding: 1rem 0;
  }

  .card-header-gradient,
  .card-body-white {
    padding: 2rem 1.5rem;
  }

  .logo-circle {
    width: 70px;
    height: 70px;
  }
}
</style>