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
                </div>

                <div class="d-grid gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading"
                  >
                    {{ isLoading ? 'Logowanie...' : 'Zaloguj się' }}
                  </button>

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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isLoading = ref(false)
const error = ref<string | null>(null)

const form = reactive({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = null

    await authStore.login(form)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd logowania'
  } finally {
    isLoading.value = false
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
</style>