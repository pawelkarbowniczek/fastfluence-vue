<template>
  <div class="activate-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="text-center mb-4">
            <h1 class="display-4 fw-bold mb-3">
              <span class="text-primary">Fast</span><span class="text-success">Fluence</span>
            </h1>
          </div>

          <div class="card shadow-lg rounded-4 p-4">
            <div class="card-body text-center">
              <!-- Loading State -->
              <div v-if="isLoading" class="loading-state">
                <div class="spinner-border text-primary mb-3" role="status">
                  <span class="visually-hidden">Ładowanie...</span>
                </div>
                <h3>Aktywacja konta...</h3>
                <p class="text-muted">Proszę czekać, sprawdzamy Twój token aktywacyjny.</p>
              </div>

              <!-- Success State -->
              <div v-else-if="activationSuccess" class="success-state">
                <div class="success-icon mb-3">
                  <i class="fas fa-check-circle fa-4x text-success"></i>
                </div>
                <h3 class="text-success">Konto aktywowane!</h3>
                <p class="text-muted mb-4">
                  Twoje konto zostało pomyślnie aktywowane. Możesz teraz zalogować się i korzystać z platformy.
                </p>
                <div class="d-grid gap-2">
                  <router-link to="/login" class="btn btn-primary btn-lg">
                    Przejdź do logowania
                  </router-link>
                  <router-link to="/" class="btn btn-outline-secondary">
                    Strona główna
                  </router-link>
                </div>
              </div>

              <!-- Error State -->
              <div v-else class="error-state">
                <div class="error-icon mb-3">
                  <i class="fas fa-exclamation-triangle fa-4x text-danger"></i>
                </div>
                <h3 class="text-danger">Błąd aktywacji</h3>
                <p class="text-muted mb-4">
                  {{ errorMessage }}
                </p>

                <div class="d-grid gap-2">
                  <button
                    @click="showResendForm = true"
                    class="btn btn-outline-primary"
                    v-if="!showResendForm"
                  >
                    Wyślij ponownie email aktywacyjny
                  </button>

                  <!-- Resend Form -->
                  <div v-if="showResendForm" class="resend-form">
                    <div class="mb-3">
                      <label for="resend-email" class="form-label">Adres email</label>
                      <input
                        v-model="resendEmail"
                        type="email"
                        class="form-control"
                        id="resend-email"
                        placeholder="Wprowadź swój email"
                        required
                      >
                    </div>
                    <div class="d-grid gap-2">
                      <button
                        @click="resendActivationEmail"
                        class="btn btn-primary"
                        :disabled="isResending || !resendEmail"
                      >
                        {{ isResending ? 'Wysyłanie...' : 'Wyślij email' }}
                      </button>
                      <button
                        @click="showResendForm = false"
                        class="btn btn-outline-secondary"
                      >
                        Anuluj
                      </button>
                    </div>
                  </div>

                  <router-link to="/register" class="btn btn-outline-secondary">
                    Zarejestruj nowe konto
                  </router-link>
                </div>
              </div>

              <!-- Resend Success Message -->
              <div v-if="resendSuccess" class="alert alert-success mt-3">
                Email aktywacyjny został wysłany ponownie. Sprawdź swoją skrzynkę pocztową.
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
  activateAccount()
})
</script>

<style scoped>
.activate-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(125, 60, 255, 0.1) 0%, rgba(212, 255, 50, 0.1) 100%);
}

.card {
  border: none;
  backdrop-filter: blur(10px);
}

.success-icon, .error-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resend-form {
  text-align: left;
  margin-top: 1rem;
}
</style>