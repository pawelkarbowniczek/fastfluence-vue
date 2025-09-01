<template>
  <div class="register-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="text-center mb-4">
            <h1 class="display-4 fw-bold mb-3">
              <span class="text-primary">Fast</span><span class="text-success">Fluence</span>
            </h1>
            <p class="fs-5 text-muted">Dołącz do platformy</p>
          </div>

          <!-- Success State - Account Created -->
          <div v-if="registrationSuccess" class="success-state">
            <div class="card shadow-lg rounded-4 p-4">
              <div class="card-body text-center">
                <div class="success-icon mb-3">
                  <i class="fas fa-envelope-circle-check fa-4x text-success"></i>
                </div>
                <h3 class="text-success">Konto utworzone!</h3>
                <p class="text-muted mb-4">
                  Twoje konto zostało utworzone pomyślnie. Wysłaliśmy email aktywacyjny na adres
                  <strong>{{ registeredEmail }}</strong>.
                </p>

                <div class="alert alert-info">
                  <i class="fas fa-info-circle me-2"></i>
                  <strong>Sprawdź swoją skrzynkę email</strong> i kliknij link aktywacyjny,
                  aby móc się zalogować.
                </div>

                <div class="d-grid gap-2">
                  <router-link to="/login" class="btn btn-primary btn-lg">
                    Przejdź do logowania
                  </router-link>
                  <router-link to="/" class="btn btn-outline-secondary">
                    Strona główna
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Registration Form -->
          <div v-else>
            <!-- Role Selection -->
            <div v-if="!selectedRole" class="role-selection mb-4">
              <h3 class="text-center mb-4">Wybierz swoją rolę</h3>
              <div class="row g-3">
                <div class="col-md-6">
                  <div
                    @click="selectRole('advertiser')"
                    class="role-card card h-100 text-center p-4 cursor-pointer"
                    :class="{ 'border-primary': hoveredRole === 'advertiser' }"
                    @mouseenter="hoveredRole = 'advertiser'"
                    @mouseleave="hoveredRole = null"
                  >
                    <div class="card-body">
                      <div class="role-icon mb-3">
                        <i class="fas fa-bullhorn fa-3x text-primary"></i>
                      </div>
                      <h5 class="card-title">Reklamodawca</h5>
                      <p class="card-text text-muted">
                        Tworzę kampanie marketingowe i szukam influencerów do współpracy
                      </p>
                    </div>
                  </div>
                </div>

                <div class="col-md-6">
                  <div
                    @click="selectRole('creator')"
                    class="role-card card h-100 text-center p-4 cursor-pointer"
                    :class="{ 'border-success': hoveredRole === 'creator' }"
                    @mouseenter="hoveredRole = 'creator'"
                    @mouseleave="hoveredRole = null"
                  >
                    <div class="card-body">
                      <div class="role-icon mb-3">
                        <i class="fas fa-star fa-3x text-success"></i>
                      </div>
                      <h5 class="card-title">Influencer</h5>
                      <p class="card-text text-muted">
                        Tworzę treści i chcę współpracować z markami
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="text-center mt-4">
                <router-link to="/login" class="text-decoration-none">
                  Masz już konto? Zaloguj się
                </router-link>
                <br>
                <router-link to="/" class="text-muted text-decoration-none">
                  ← Powrót do strony głównej
                </router-link>
              </div>
            </div>

            <!-- Registration Form -->
            <div v-else class="registration-form">
              <div class="card shadow-lg rounded-4 p-4">
                <div class="card-body">
                  <div class="d-flex align-items-center mb-4">
                    <button
                      @click="selectedRole = null"
                      class="btn btn-outline-secondary btn-sm me-3"
                    >
                      ← Zmień rolę
                    </button>
                    <h3 class="mb-0">
                      Rejestracja {{ selectedRole === 'advertiser' ? 'Reklamodawcy' : 'Influencera' }}
                    </h3>
                  </div>

                  <form @submit.prevent="handleSubmit">
                    <div class="row">
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="email" class="form-label">Email</label>
                          <input
                            v-model="form.email"
                            type="email"
                            class="form-control"
                            id="email"
                            required
                          >
                        </div>
                      </div>

                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="password" class="form-label">Hasło</label>
                          <input
                            v-model="form.password"
                            type="password"
                            class="form-control"
                            id="password"
                            required
                          >
                        </div>
                      </div>
                    </div>

                    <div class="row">
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="display_name" class="form-label">Nazwa wyświetlana</label>
                          <input
                            v-model="form.display_name"
                            type="text"
                            class="form-control"
                            id="display_name"
                            required
                          >
                        </div>
                      </div>

                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="contact_email" class="form-label">Email kontaktowy</label>
                          <input
                            v-model="form.contact_email"
                            type="email"
                            class="form-control"
                            id="contact_email"
                            required
                          >
                        </div>
                      </div>
                    </div>

                    <div class="row">
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="phone" class="form-label">Telefon (opcjonalnie)</label>
                          <input
                            v-model="form.phone"
                            type="tel"
                            class="form-control"
                            id="phone"
                          >
                        </div>
                      </div>

                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="website_url" class="form-label">Strona internetowa (opcjonalnie)</label>
                          <input
                            v-model="form.website_url"
                            type="url"
                            class="form-control"
                            id="website_url"
                          >
                        </div>
                      </div>
                    </div>

                    <div v-if="error" class="alert alert-danger">
                      {{ error }}
                    </div>

                    <div class="d-grid gap-2">
                      <button
                        type="submit"
                        class="btn btn-primary btn-lg"
                        :disabled="isLoading"
                      >
                        {{ isLoading ? 'Rejestracja...' : 'Zarejestruj się' }}
                      </button>

                      <div class="text-center mt-3">
                        <router-link to="/login" class="text-decoration-none">
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import type { UserRole } from '../types'

interface Props {
  role?: string
}

const props = defineProps<Props>()

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const selectedRole = ref<UserRole | null>(null)
const hoveredRole = ref<UserRole | null>(null)
const isLoading = ref(false)
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

onMounted(() => {
  if (props.role && ['advertiser', 'creator'].includes(props.role)) {
    selectRole(props.role as UserRole)
  }
})
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding: 2rem 0;
  background: linear-gradient(135deg, rgba(125, 60, 255, 0.1) 0%, rgba(212, 255, 50, 0.1) 100%);
}

.role-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.role-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.role-card.border-primary {
  border-color: var(--violet) !important;
}

.role-card.border-success {
  border-color: var(--lime) !important;
}

.cursor-pointer {
  cursor: pointer;
}

.card {
  border: none;
  backdrop-filter: blur(10px);
}

.role-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>