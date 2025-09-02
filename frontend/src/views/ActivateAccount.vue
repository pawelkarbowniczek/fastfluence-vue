<template>
  <div class="activate-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <!-- Logo Section -->
          <div class="text-center mb-4">
            <div class="logo-section">
              <div class="logo-circle mb-3">
                <i class="fas fa-envelope-open-text fa-2x"></i>
              </div>
              <h1 class="display-4 fw-bold mb-3 text-white">
                <span style="color: var(--violet);">Fast</span><span style="color: var(--lime);">Fluence</span>
              </h1>
            </div>
          </div>

          <!-- Activation Card -->
          <div class="activation-card">
            <!-- Loading State -->
            <div v-if="isLoading" class="card-header-loading text-white text-center">
              <div class="loading-icon mb-3">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Ładowanie...</span>
                </div>
              </div>
              <h3 class="mb-0 fw-bold">Aktywacja konta...</h3>
              <p class="mb-0 opacity-75">Proszę czekać, sprawdzamy Twój token aktywacyjny</p>
            </div>

            <!-- Success State -->
            <div v-else-if="activationSuccess" class="card-header-success text-white text-center">
              <div class="success-icon mb-3">
                <i class="fas fa-check-circle fa-4x"></i>
              </div>
              <h3 class="mb-0 fw-bold">Konto aktywowane!</h3>
              <p class="mb-0 opacity-75">Możesz teraz korzystać z platformy</p>
            </div>

            <!-- Error State -->
            <div v-else class="card-header-error text-white text-center">
              <div class="error-icon mb-3">
                <i class="fas fa-exclamation-triangle fa-4x"></i>
              </div>
              <h3 class="mb-0 fw-bold">Błąd aktywacji</h3>
              <p class="mb-0 opacity-75">Token jest nieprawidłowy lub wygasł</p>
            </div>

            <!-- Card Body -->
            <div class="card-body-white">
              <!-- Loading Content -->
              <div v-if="isLoading" class="text-center">
                <div class="loading-progress mb-3">
                  <div class="progress">
                    <div class="progress-bar progress-bar-animated"
                         role="progressbar"
                         style="width: 100%"></div>
                  </div>
                </div>
                <p class="text-muted">Weryfikujemy Twój token aktywacyjny...</p>
              </div>

              <!-- Success Content -->
              <div v-else-if="activationSuccess" class="text-center">
                <div class="success-message mb-4">
                  <h5 class="text-success mb-3">
                    <i class="fas fa-party-horn me-2"></i>
                    Witamy w FastFluence!
                  </h5>
                  <p class="text-muted">
                    Twoje konto zostało pomyślnie aktywowane. Możesz teraz zalogować się
                    i korzystać ze wszystkich funkcji platformy.
                  </p>
                </div>

                <div class="d-grid gap-2">
                  <router-link to="/login" class="btn btn-primary-gradient btn-lg">
                    <i class="fas fa-sign-in-alt me-2"></i>
                    Przejdź do logowania
                  </router-link>
                  <router-link to="/" class="btn btn-outline-secondary">
                    <i class="fas fa-home me-2"></i>
                    Strona główna
                  </router-link>
                </div>
              </div>

              <!-- Error Content -->
              <div v-else class="text-center">
                <div class="error-message mb-4">
                  <p class="text-danger fw-semibold mb-3">
                    {{ errorMessage }}
                  </p>
                  <p class="text-muted small">
                    Token aktywacyjny może wygasnąć po 24 godzinach od wysłania emaila.
                  </p>
                </div>

                <!-- Resend Form -->
                <div v-if="!showResendForm" class="d-grid gap-2 mb-3">
                  <button
                    @click="showResendForm = true"
                    class="btn btn-outline-primary"
                  >
                    <i class="fas fa-paper-plane me-2"></i>
                    Wyślij ponownie email aktywacyjny
                  </button>
                </div>

                <div v-else class="resend-section mb-4">
                  <div class="resend-form-card">
                    <h6 class="fw-bold mb-3">
                      <i class="fas fa-envelope me-2"></i>
                      Ponowne wysłanie emaila
                    </h6>

                    <div class="mb-3">
                      <label for="resend-email" class="form-label">Adres email</label>
                      <input
                        v-model="resendEmail"
                        type="email"
                        class="form-control form-control-custom"
                        id="resend-email"
                        placeholder="Wprowadź swój email"
                        required
                      >
                    </div>

                    <div class="d-grid gap-2">
                      <button
                        @click="resendActivationEmail"
                        class="btn btn-primary-gradient"
                        :disabled="isResending || !resendEmail"
                      >
                        <i class="fas fa-paper-plane me-2"></i>
                        {{ isResending ? 'Wysyłanie...' : 'Wyślij email' }}
                      </button>
                      <button
                        @click="showResendForm = false"
                        class="btn btn-outline-secondary"
                      >
                        <i class="fas fa-times me-2"></i>
                        Anuluj
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Alternative Actions -->
                <div class="d-grid gap-2">
                  <router-link to="/register" class="btn btn-outline-secondary">
                    <i class="fas fa-user-plus me-2"></i>
                    Zarejestruj nowe konto
                  </router-link>
                  <router-link to="/" class="btn btn-outline-light">
                    <i class="fas fa-home me-2"></i>
                    Strona główna
                  </router-link>
                </div>

                <!-- Resend Success Message -->
                <div v-if="resendSuccess" class="alert alert-success-custom mt-4">
                  <i class="fas fa-check-circle me-2"></i>
                  <strong>Email wysłany!</strong> Sprawdź swoją skrzynkę pocztową.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authApi } from '../services/api'

const route = useRoute()

const isLoading = ref(true)
const activationSuccess = ref(false)
const errorMessage = ref('')
const showResendForm = ref(false)
const resendEmail = ref('')
const isResending = ref(false)
const resendSuccess = ref(false)

const activateAccount = async () => {
  const token = route.params.token as string

  if (!token) {
    isLoading.value = false
    errorMessage.value = 'Brak tokenu aktywacyjnego w adresie URL.'
    return
  }

  try {
    await authApi.activateAccount(token)
    activationSuccess.value = true
  } catch (err: any) {
    errorMessage.value = err.response?.data?.detail || 'Token aktywacyjny jest nieprawidłowy lub wygasł.'
  } finally {
    isLoading.value = false
  }
}

const resendActivationEmail = async () => {
  if (!resendEmail.value) return

  try {
    isResending.value = true
    await authApi.resendActivation(resendEmail.value)
    resendSuccess.value = true
    showResendForm.value = false
  } catch (err: any) {
    errorMessage.value = err.response?.data?.detail || 'Błąd wysyłania emaila aktywacyjnego.'
  } finally {
    isResending.value = false
  }
}

onMounted(() => {
  // Delay activation for better UX
  setTimeout(() => {
    activateAccount()
  }, 1500)
})
</script>

<style scoped>
.activate-page {
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

.activation-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.card-header-loading {
  background: linear-gradient(135deg, #17a2b8 0%, #20c997 100%);
  padding: 2.5rem 2rem;
  border-bottom: none;
}

.card-header-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  padding: 2.5rem 2rem;
  border-bottom: none;
}

.card-header-error {
  background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
  padding: 2.5rem 2rem;
  border-bottom: none;
}

.card-body-white {
  background: white;
  padding: 2.5rem;
}

.loading-icon,
.success-icon,
.error-icon {
  display: inline-block;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3em;
}

.loading-progress .progress {
  height: 6px;
  border-radius: 3px;
  background-color: rgba(125, 60, 255, 0.1);
}

.progress-bar {
  background: linear-gradient(90deg, var(--violet), var(--lime));
  border-radius: 3px;
}

.success-message,
.error-message {
  padding: 1rem 0;
}

.resend-section {
  text-align: left;
}

.resend-form-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
}

.form-control-custom {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-control-custom:focus {
  border-color: var(--violet);
  box-shadow: 0 0 0 0.2rem rgba(125, 60, 255, 0.15);
}

.btn-primary-gradient {
  background: linear-gradient(135deg, var(--violet) 0%, #6B2FDB 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.btn-primary-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(125, 60, 255, 0.3);
  color: white;
}

.btn-primary-gradient:disabled {
  opacity: 0.7;
  transform: none;
}

.btn-outline-secondary {
  border: 2px solid #6c757d;
  color: #6c757d;
  background: transparent;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  background: #6c757d;
  border-color: #6c757d;
  color: white;
}

.btn-outline-primary {
  border: 2px solid var(--violet);
  color: var(--violet);
  background: transparent;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: var(--violet);
  border-color: var(--violet);
  color: white;
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  font-weight: 500;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
}

.alert-success-custom {
  background: rgba(25, 135, 84, 0.1);
  color: #0a3622;
  border: none;
  border-left: 4px solid #198754;
  border-radius: 10px;
  padding: 1rem 1.25rem;
}

@media (max-width: 768px) {
  .activate-page {
    padding: 1rem 0;
  }

  .card-header-loading,
  .card-header-success,
  .card-header-error,
  .card-body-white {
    padding: 2rem 1.5rem;
  }

  .logo-circle {
    width: 70px;
    height: 70px;
  }
}
</style>