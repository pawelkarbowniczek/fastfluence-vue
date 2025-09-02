<template>
  <div class="register-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-10 col-lg-8">
          <!-- Logo Section -->
          <div class="text-center mb-4">
            <div class="logo-section">
              <div class="logo-circle mb-3">
                <i class="fas fa-user-plus fa-2x"></i>
              </div>
              <h1 class="display-4 fw-bold mb-3 text-white">
                <span style="color: var(--violet);">Fast</span><span style="color: var(--lime);">Fluence</span>
              </h1>
              <p class="fs-5 text-white opacity-75">Dołącz do platformy</p>
            </div>
          </div>

          <!-- Success State -->
          <div v-if="registrationSuccess" class="success-card">
            <div class="card-header-success text-white text-center">
              <div class="success-icon mb-3">
                <i class="fas fa-envelope-circle-check fa-4x"></i>
              </div>
              <h3 class="mb-0 fw-bold">Konto utworzone!</h3>
              <p class="mb-0 opacity-75">Email aktywacyjny został wysłany</p>
            </div>

            <div class="card-body-white">
              <div class="text-center">
                <p class="text-muted mb-3">
                  Twoje konto zostało utworzone pomyślnie. Wysłaliśmy email aktywacyjny na adres
                  <strong class="text-primary">{{ registeredEmail }}</strong>.
                </p>

                <div class="alert alert-info-custom mb-4">
                  <i class="fas fa-info-circle me-2"></i>
                  <strong>Sprawdź swoją skrzynkę email</strong> i kliknij link aktywacyjny,
                  aby móc się zalogować.
                </div>

                <div class="d-grid gap-2">
                  <router-link to="/login" class="btn btn-primary-gradient btn-lg">
                    <i class="fas fa-sign-in-alt me-2"></i>
                    Przejdź do logowania
                  </router-link>
                  <router-link to="/" class="btn btn-outline-light">
                    <i class="fas fa-home me-2"></i>
                    Strona główna
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Registration Form -->
          <div v-else class="register-card">
            <!-- Role Selection -->
            <div v-if="!selectedRole" class="role-selection-card">
              <div class="card-header-gradient text-white text-center">
                <h3 class="mb-0 fw-bold">Wybierz swoją rolę</h3>
                <p class="mb-0 opacity-75">Kim jesteś w świecie marketingu?</p>
              </div>

              <div class="card-body-white">
                <div class="row g-4 mb-4">
                  <div class="col-md-6">
                    <div
                      @click="selectRole('advertiser')"
                      class="role-card"
                      :class="{ 'role-card-hover': hoveredRole === 'advertiser' }"
                      @mouseenter="hoveredRole = 'advertiser'"
                      @mouseleave="hoveredRole = null"
                    >
                      <div class="role-icon mb-3">
                        <i class="fas fa-bullhorn fa-3x"></i>
                      </div>
                      <h5 class="fw-bold">Reklamodawca</h5>
                      <p class="text-muted mb-3">
                        Tworzę kampanie marketingowe i szukam influencerów do współpracy
                      </p>
                      <ul class="role-features">
                        <li><i class="fas fa-check me-2"></i>Publikuj kampanie</li>
                        <li><i class="fas fa-check me-2"></i>Znajdź twórców</li>
                        <li><i class="fas fa-check me-2"></i>Zarządzaj projektami</li>
                      </ul>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div
                      @click="selectRole('creator')"
                      class="role-card"
                      :class="{ 'role-card-hover': hoveredRole === 'creator' }"
                      @mouseenter="hoveredRole = 'creator'"
                      @mouseleave="hoveredRole = null"
                    >
                      <div class="role-icon mb-3">
                        <i class="fas fa-star fa-3x"></i>
                      </div>
                      <h5 class="fw-bold">Influencer</h5>
                      <p class="text-muted mb-3">
                        Tworzę treści i chcę współpracować z markami
                      </p>
                      <ul class="role-features">
                        <li><i class="fas fa-check me-2"></i>Przeglądaj kampanie</li>
                        <li><i class="fas fa-check me-2"></i>Aplikuj do projektów</li>
                        <li><i class="fas fa-check me-2"></i>Buduj portfolio</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <!-- Auth0 Quick Registration -->
                <div class="auth0-section">
                  <div class="divider-custom">
                    <span class="divider-text">lub skorzystaj z szybkiej rejestracji</span>
                  </div>

                  <div class="row g-2">
                    <div class="col-md-6">
                      <button
                        type="button"
                        @click="loginWithAuth0('advertiser')"
                        class="btn btn-auth0-advertiser w-100"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-bullhorn me-2"></i>
                        Reklamodawca przez Auth0
                      </button>
                    </div>
                    <div class="col-md-6">
                      <button
                        type="button"
                        @click="loginWithAuth0('creator')"
                        class="btn btn-auth0-creator w-100"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-star me-2"></i>
                        Influencer przez Auth0
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Footer Links -->
                <div class="text-center mt-4">
                  <div class="link-section">
                    <router-link to="/login" class="link-custom">
                      Masz już konto? Zaloguj się
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
            </div>

            <!-- Registration Form -->
            <div v-else class="registration-form-card">
              <div class="card-header-gradient text-white">
                <div class="d-flex align-items-center">
                  <button
                    @click="selectedRole = null"
                    class="btn btn-outline-light btn-sm me-3"
                  >
                    <i class="fas fa-arrow-left me-1"></i>
                    Zmień rolę
                  </button>
                  <div>
                    <h3 class="mb-1 fw-bold">
                      Rejestracja {{ selectedRole === 'advertiser' ? 'Reklamodawcy' : 'Influencera' }}
                    </h3>
                    <p class="mb-0 opacity-75">Wypełnij swoje dane osobowe</p>
                  </div>
                </div>
              </div>

              <div class="card-body-white">
                <form @submit.prevent="handleSubmit">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label for="email" class="form-label fw-semibold">
                        <i class="fas fa-envelope me-2 text-primary"></i>
                        Email
                      </label>
                      <input
                        v-model="form.email"
                        type="email"
                        class="form-control form-control-custom"
                        id="email"
                        placeholder="twoj@email.com"
                        required
                      >
                    </div>

                    <div class="col-md-6">
                      <label for="password" class="form-label fw-semibold">
                        <i class="fas fa-lock me-2 text-primary"></i>
                        Hasło
                      </label>
                      <input
                        v-model="form.password"
                        type="password"
                        class="form-control form-control-custom"
                        id="password"
                        placeholder="Wprowadź hasło"
                        required
                      >
                    </div>

                    <div class="col-md-6">
                      <label for="display_name" class="form-label fw-semibold">
                        <i class="fas fa-user me-2 text-primary"></i>
                        Nazwa wyświetlana
                      </label>
                      <input
                        v-model="form.display_name"
                        type="text"
                        class="form-control form-control-custom"
                        id="display_name"
                        placeholder="Jak chcesz być nazywany?"
                        required
                      >
                    </div>

                    <div class="col-md-6">
                      <label for="contact_email" class="form-label fw-semibold">
                        <i class="fas fa-at me-2 text-primary"></i>
                        Email kontaktowy
                      </label>
                      <input
                        v-model="form.contact_email"
                        type="email"
                        class="form-control form-control-custom"
                        id="contact_email"
                        placeholder="kontakt@email.com"
                        required
                      >
                    </div>

                    <div class="col-md-6">
                      <label for="phone" class="form-label fw-semibold">
                        <i class="fas fa-phone me-2 text-muted"></i>
                        Telefon <small class="text-muted">(opcjonalnie)</small>
                      </label>
                      <input
                        v-model="form.phone"
                        type="tel"
                        class="form-control form-control-custom"
                        id="phone"
                        placeholder="+48 123 456 789"
                      >
                    </div>

                    <div class="col-md-6">
                      <label for="website_url" class="form-label fw-semibold">
                        <i class="fas fa-globe me-2 text-muted"></i>
                        Strona internetowa <small class="text-muted">(opcjonalnie)</small>
                      </label>
                      <input
                        v-model="form.website_url"
                        type="url"
                        class="form-control form-control-custom"
                        id="website_url"
                        placeholder="https://twoja-strona.pl"
                      >
                    </div>
                  </div>

                  <div v-if="error" class="alert alert-danger alert-custom mt-4">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    {{ error }}
                  </div>

                  <div class="d-grid gap-3 mt-4">
                    <button
                      type="submit"
                      class="btn btn-primary-gradient btn-lg"
                      :disabled="isLoading"
                    >
                      <i class="fas fa-user-plus me-2"></i>
                      {{ isLoading ? 'Rejestracja...' : 'Zarejestruj się' }}
                    </button>

                    <!-- Auth0 Alternative -->
                    <div class="auth0-section">
                      <div class="divider-custom">
                        <span class="divider-text">lub kontynuuj z</span>
                      </div>

                      <button
                        type="button"
                        @click="loginWithAuth0(selectedRole)"
                        class="btn btn-outline-secondary btn-lg w-100"
                        :disabled="isAuth0Loading"
                      >
                        <i class="fas fa-sign-in-alt me-2"></i>
                        Kontynuuj przez Auth0
                      </button>
                    </div>

                    <div class="text-center mt-3">
                      <router-link to="/login" class="link-custom">
                        Masz już konto? Zaloguj się
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAuth0Store } from '../stores/auth0'
import type { UserRole } from '../types'

interface Props {
  role?: string
}

const props = defineProps<Props>()

const authStore = useAuthStore()
const auth0Store = useAuth0Store()
const router = useRouter()
const route = useRoute()

const selectedRole = ref<UserRole | null>(null)
const hoveredRole = ref<UserRole | null>(null)
const isLoading = ref(false)
const isAuth0Loading = ref(false)
const error = ref<string | null>(null)
const registrationSuccess = ref(false)
const registeredEmail = ref('')

const form = reactive({
  email: '',
  password: '',
  display_name: '',
  contact_email: '',
  phone: '',
  website_url: '',
  role: 'advertiser' as UserRole,
  social_links: [],
  portfolio: []
})

const selectRole = (role: UserRole) => {
  selectedRole.value = role
  form.role = role
  router.replace(`/register/${role}`)
}

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = null

    if (!form.contact_email) {
      form.contact_email = form.email
    }

    await authStore.register(form)
    registeredEmail.value = form.email
    registrationSuccess.value = true
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd rejestracji'
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

onMounted(() => {
  if (props.role && ['advertiser', 'creator'].includes(props.role)) {
    selectRole(props.role as UserRole)
  }
})
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.register-card,
.success-card {
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

.card-header-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  padding: 2.5rem 2rem;
  border-bottom: none;
}

.card-body-white {
  background: white;
  padding: 2.5rem;
}

.success-icon {
  display: inline-block;
}

.role-selection-card,
.registration-form-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.role-card {
  background: #f8f9fa;
  border: 3px solid #e9ecef;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.role-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--violet) 0%, var(--lime) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.role-card-hover::before {
  opacity: 0.05;
}

.role-card-hover {
  border-color: var(--violet);
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(125, 60, 255, 0.2);
}

.role-icon {
  position: relative;
  z-index: 2;
  color: var(--violet);
}

.role-card-hover .role-icon {
  color: var(--violet);
  transform: scale(1.1);
}

.role-features {
  list-style: none;
  padding: 0;
  position: relative;
  z-index: 2;
}

.role-features li {
  padding: 0.25rem 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.role-features .fas.fa-check {
  color: #28a745;
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

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
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

.alert-info-custom {
  background: rgba(13, 202, 240, 0.1);
  color: #055160;
  border-left: 4px solid #0dcaf0;
  border-radius: 10px;
  padding: 1rem 1.25rem;
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
  .register-page {
    padding: 1rem 0;
  }

  .card-header-gradient,
  .card-header-success,
  .card-body-white {
    padding: 2rem 1.5rem;
  }

  .logo-circle {
    width: 70px;
    height: 70px;
  }

  .role-card {
    padding: 1.5rem;
  }
}
</style>