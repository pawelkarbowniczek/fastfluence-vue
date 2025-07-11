<template>
  <ModalBase @close="$emit('close')">
    <div class="modal-header">
      <h5 class="modal-title">Logowanie</h5>
      <button type="button" class="btn-close" @click="$emit('close')"></button>
    </div>
    
    <div class="modal-body">
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
        
        <div class="d-grid">
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Logowanie...' : 'Zaloguj się' }}
          </button>
        </div>
      </form>
    </div>
  </ModalBase>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ModalBase from './ModalBase.vue'

const emit = defineEmits<{
  close: []
  success: []
}>()

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
    emit('success')
    emit('close')
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd logowania'
  } finally {
    isLoading.value = false
  }
}
</script>