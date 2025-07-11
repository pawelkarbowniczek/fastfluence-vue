<template>
  <div class="card shadow-lg rounded-4 p-4 mx-auto" style="max-width: 28rem;">
    <div class="card-body">
      <h3 class="card-title text-center mb-4">
        Rejestracja {{ role === 'advertiser' ? 'Reklamodawcy' : 'Influencera' }}
      </h3>
      
      <form @submit.prevent="handleSubmit">
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
        
        <div class="mb-3">
          <label for="phone" class="form-label">Telefon</label>
          <input 
            v-model="form.phone" 
            type="tel" 
            class="form-control" 
            id="phone"
          >
        </div>
        
        <div class="mb-3">
          <label for="website_url" class="form-label">Strona internetowa</label>
          <input 
            v-model="form.website_url" 
            type="url" 
            class="form-control" 
            id="website_url"
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
            {{ isLoading ? 'Rejestracja...' : 'Zarejestruj się' }}
          </button>
          
          <button 
            type="button" 
            class="btn btn-outline-secondary"
            @click="showLogin = true"
          >
            Masz już konto? Zaloguj się
          </button>
        </div>
      </form>
    </div>
    
    <AuthLogin 
      v-if="showLogin"
      @close="showLogin = false"
      @success="$emit('success')"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import AuthLogin from './AuthLogin.vue'
import type { UserRole } from '../types'

interface Props {
  role: UserRole
}

const props = defineProps<Props>()
const emit = defineEmits<{
  success: []
}>()

const authStore = useAuthStore()
const router = useRouter()

const showLogin = ref(false)
const isLoading = ref(false)
const error = ref<string | null>(null)

const form = reactive({
  email: '',
  password: '',
  display_name: '',
  contact_email: '',
  phone: '',
  website_url: '',
  role: props.role,
  social_links: [],
  portfolio: []
})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    if (!form.contact_email) {
      form.contact_email = form.email
    }
    
    await authStore.register(form)
    emit('success')
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd rejestracji'
  } finally {
    isLoading.value = false
  }
}
</script>