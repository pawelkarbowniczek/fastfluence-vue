<template>
  <div class="profile-page">
    <div class="container py-4">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h2 class="mb-0">Mój profil</h2>
            </div>
            
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
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
                      <label for="phone" class="form-label">Telefon</label>
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
                      <label for="website_url" class="form-label">Strona internetowa</label>
                      <input 
                        v-model="form.website_url" 
                        type="url" 
                        class="form-control" 
                        id="website_url"
                      >
                    </div>
                  </div>
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Media społecznościowe</label>
                  <div class="social-links-container">
                    <div 
                      v-for="(link, index) in form.social_links" 
                      :key="index"
                      class="input-group mb-2"
                    >
                      <input 
                        v-model="form.social_links[index]" 
                        type="url" 
                        class="form-control" 
                        placeholder="https://instagram.com/username"
                      >
                      <button 
                        type="button" 
                        class="btn btn-outline-danger"
                        @click="removeSocialLink(index)"
                      >
                        Usuń
                      </button>
                    </div>
                    <button 
                      type="button" 
                      class="btn btn-outline-primary btn-sm"
                      @click="addSocialLink"
                    >
                      Dodaj link
                    </button>
                  </div>
                </div>
                
                <div v-if="isCreator" class="mb-3">
                  <label class="form-label">Portfolio</label>
                  <div class="portfolio-container">
                    <div 
                      v-for="(item, index) in form.portfolio" 
                      :key="index"
                      class="card mb-3"
                    >
                      <div class="card-body">
                        <div class="row">
                          <div class="col-md-6">
                            <div class="mb-2">
                              <label class="form-label small">Tytuł projektu</label>
                              <input 
                                v-model="item.title" 
                                type="text" 
                                class="form-control form-control-sm"
                                required
                              >
                            </div>
                          </div>
                          
                          <div class="col-md-6">
                            <div class="mb-2">
                              <label class="form-label small">Nazwa marki</label>
                              <input 
                                v-model="item.brand_name" 
                                type="text" 
                                class="form-control form-control-sm"
                                required
                              >
                            </div>
                          </div>
                        </div>
                        
                        <div class="row">
                          <div class="col-md-6">
                            <div class="mb-2">
                              <label class="form-label small">Rola w kampanii</label>
                              <input 
                                v-model="item.role_in_campaign" 
                                type="text" 
                                class="form-control form-control-sm"
                                required
                              >
                            </div>
                          </div>
                          
                          <div class="col-md-6">
                            <div class="mb-2">
                              <label class="form-label small">Link do projektu</label>
                              <input 
                                v-model="item.landing_url" 
                                type="url" 
                                class="form-control form-control-sm"
                              >
                            </div>
                          </div>
                        </div>
                        
                        <div class="mb-2">
                          <label class="form-label small">Krótki opis (max 280 znaków)</label>
                          <textarea 
                            v-model="item.short_description" 
                            class="form-control form-control-sm"
                            maxlength="280"
                            rows="2"
                            required
                          ></textarea>
                          <div class="text-muted small">
                            {{ item.short_description.length }}/280
                          </div>
                        </div>
                        
                        <div class="text-end">
                          <button 
                            type="button" 
                            class="btn btn-outline-danger btn-sm"
                            @click="removePortfolioItem(index)"
                          >
                            Usuń projekt
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <button 
                      type="button" 
                      class="btn btn-outline-primary btn-sm"
                      @click="addPortfolioItem"
                    >
                      Dodaj projekt
                    </button>
                  </div>
                </div>
                
                <div v-if="error" class="alert alert-danger">
                  {{ error }}
                </div>
                
                <div v-if="success" class="alert alert-success">
                  Profil został zaktualizowany pomyślnie!
                </div>
                
                <div class="d-flex gap-2">
                  <button 
                    type="submit" 
                    class="btn btn-primary"
                    :disabled="isLoading"
                  >
                    {{ isLoading ? 'Zapisywanie...' : 'Zapisz zmiany' }}
                  </button>
                  
                  <button 
                    type="button" 
                    class="btn btn-outline-secondary"
                    @click="resetForm"
                  >
                    Resetuj
                  </button>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import type { PortfolioCampaign } from '../types'

const authStore = useAuthStore()

const isCreator = computed(() => authStore.isCreator)
const isLoading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

const form = reactive({
  display_name: '',
  contact_email: '',
  phone: '',
  website_url: '',
  social_links: [] as string[],
  portfolio: [] as PortfolioCampaign[]
})

const initializeForm = () => {
  if (authStore.user) {
    form.display_name = authStore.user.display_name
    form.contact_email = authStore.user.contact_email
    form.phone = authStore.user.phone || ''
    form.website_url = authStore.user.website_url || ''
    form.social_links = [...authStore.user.social_links]
    form.portfolio = [...authStore.user.portfolio]
  }
}

const addSocialLink = () => {
  form.social_links.push('')
}

const removeSocialLink = (index: number) => {
  form.social_links.splice(index, 1)
}

const addPortfolioItem = () => {
  form.portfolio.push({
    title: '',
    brand_name: '',
    role_in_campaign: '',
    landing_url: '',
    cover_image_url: '',
    short_description: ''
  })
}

const removePortfolioItem = (index: number) => {
  form.portfolio.splice(index, 1)
}

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = null
    success.value = false
    
    // Filter out empty social links
    const cleanedSocialLinks = form.social_links.filter(link => link.trim())
    
    const updateData = {
      display_name: form.display_name,
      contact_email: form.contact_email,
      phone: form.phone || undefined,
      website_url: form.website_url || undefined,
      social_links: cleanedSocialLinks,
      portfolio: form.portfolio
    }
    
    await authStore.updateProfile(updateData)
    success.value = true
    
    setTimeout(() => {
      success.value = false
    }, 3000)
    
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd aktualizacji profilu'
  } finally {
    isLoading.value = false
  }
}

const resetForm = () => {
  initializeForm()
  error.value = null
  success.value = false
}

onMounted(() => {
  initializeForm()
})
</script>

<style scoped>
.profile-page {
  min-height: 80vh;
}

.social-links-container, .portfolio-container {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  padding: 1rem;
  background-color: #f8f9fa;
}

.portfolio-container .card {
  border: 1px solid #dee2e6;
  background-color: white;
}
</style>