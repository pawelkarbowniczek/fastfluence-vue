<template>
  <div class="add-campaign-page">
    <div class="container py-4">
      <!-- Elegant breadcrumb -->
      <div class="campaign-navigation mb-4">
        <router-link
          to="/dashboard"
          class="back-button"
          title="Powrót do dashboard"
        >
          <i class="fas fa-arrow-left me-2"></i>
          Powrót do Dashboard
        </router-link>
      </div>

      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow-lg campaign-card">
            <div class="card-header bg-gradient-primary text-white text-center position-relative">
              <div class="campaign-header-content">
                <div class="campaign-icon mb-2">
                  <div class="icon-circle">
                    <i class="fas fa-plus fa-2x"></i>
                  </div>
                </div>
                <h2 class="mb-0 campaign-title">{{ isEditing ? 'Edytuj kampanię' : 'Dodaj nową kampanię' }}</h2>
                <p class="mb-0 opacity-75">Wypełnij szczegóły swojej kampanii marketingowej</p>
              </div>

              <router-link
                to="/dashboard"
                class="campaign-close-btn"
                title="Zamknij"
              >
                <i class="fas fa-times"></i>
              </router-link>
            </div>

            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="title" class="form-label">Tytuł kampanii</label>
                      <input
                        v-model="form.title"
                        type="text"
                        class="form-control"
                        id="title"
                        required
                        placeholder="Wprowadź tytuł kampanii"
                      >
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="category" class="form-label">Kategoria</label>
                      <select v-model="form.category" class="form-select" id="category" required>
                        <option value="">Wybierz kategorię</option>
                        <option value="Moda">Moda</option>
                        <option value="Technologia">Technologia</option>
                        <option value="Kulinaria">Kulinaria</option>
                        <option value="Fitness">Fitness</option>
                        <option value="Podróże">Podróże</option>
                        <option value="Lifestyle">Lifestyle</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="description" class="form-label">Opis kampanii</label>
                  <textarea
                    v-model="form.description"
                    class="form-control"
                    id="description"
                    rows="4"
                    required
                    placeholder="Opisz szczegóły kampanii, oczekiwania i wymagania"
                  ></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="media_channel" class="form-label">Kanał mediowy</label>
                      <select v-model="form.media_channel" class="form-select" id="media_channel" required>
                        <option value="">Wybierz kanał</option>
                        <option value="Instagram">Instagram</option>
                        <option value="TikTok">TikTok</option>
                        <option value="YouTube">YouTube</option>
                        <option value="Blog">Blog</option>
                        <option value="Facebook">Facebook</option>
                        <option value="LinkedIn">LinkedIn</option>
                        <option value="Other">Inne</option>
                      </select>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="mb-3">
                      <label for="location" class="form-label">Lokalizacja</label>
                      <input
                        v-model="form.location"
                        type="text"
                        class="form-control"
                        id="location"
                        required
                        placeholder="np. Warszawa, Cała Polska"
                      >
                    </div>
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label">Typ wynagrodzenia</label>
                  <div class="compensation-options">
                    <div class="form-check">
                      <input
                        v-model="form.compensation"
                        class="form-check-input"
                        type="radio"
                        value="Cash"
                        id="compensation-cash"
                      >
                      <label class="form-check-label" for="compensation-cash">
                        <i class="fas fa-money-bill-wave me-2 text-success"></i>
                        Gotówka
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        v-model="form.compensation"
                        class="form-check-input"
                        type="radio"
                        value="Barter"
                        id="compensation-barter"
                      >
                      <label class="form-check-label" for="compensation-barter">
                        <i class="fas fa-handshake me-2 text-primary"></i>
                        Barter
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        v-model="form.compensation"
                        class="form-check-input"
                        type="radio"
                        value="Mixed"
                        id="compensation-mixed"
                      >
                      <label class="form-check-label" for="compensation-mixed">
                        <i class="fas fa-coins me-2 text-warning"></i>
                        Mieszane
                      </label>
                    </div>
                  </div>
                </div>

                <div v-if="showBudgetFields" class="budget-section mb-4">
                  <h6 class="text-primary mb-3">
                    <i class="fas fa-calculator me-2"></i>
                    Budżet kampanii
                  </h6>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label for="budget_min" class="form-label">Budżet minimalny (PLN)</label>
                        <input
                          v-model.number="form.budget_min"
                          type="number"
                          class="form-control"
                          id="budget_min"
                          min="0"
                          step="100"
                          :required="requiresBudget"
                          placeholder="1000"
                        >
                      </div>
                    </div>

                    <div class="col-md-6">
                      <div class="mb-3">
                        <label for="budget_max" class="form-label">Budżet maksymalny (PLN)</label>
                        <input
                          v-model.number="form.budget_max"
                          type="number"
                          class="form-control"
                          id="budget_max"
                          min="0"
                          step="100"
                          :required="requiresBudget"
                          placeholder="5000"
                        >
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="showBarterField" class="barter-section mb-4">
                  <h6 class="text-primary mb-3">
                    <i class="fas fa-gift me-2"></i>
                    Szczegóły barteru
                  </h6>
                  <div class="mb-3">
                    <label for="barter_descr" class="form-label">Opis oferty barterowej</label>
                    <textarea
                      v-model="form.barter_descr"
                      class="form-control"
                      id="barter_descr"
                      rows="3"
                      :required="requiresBarter"
                      placeholder="Opisz co oferujesz w zamian za promocję (produkty, usługi, doświadczenia)"
                    ></textarea>
                  </div>
                </div>

                <div class="mb-4">
                  <label for="deadline" class="form-label">
                    <i class="fas fa-calendar me-2"></i>
                    Deadline kampanii
                  </label>
                  <input
                    v-model="form.deadline"
                    type="datetime-local"
                    class="form-control"
                    id="deadline"
                    required
                  >
                </div>

                <div v-if="error" class="alert alert-danger">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>

                <div v-if="success" class="alert alert-success">
                  <i class="fas fa-check-circle me-2"></i>
                  Kampania została {{ isEditing ? 'zaktualizowana' : 'utworzona' }} pomyślnie!
                </div>

                <div class="d-flex gap-3">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg px-4"
                    :disabled="isLoading"
                  >
                    <i class="fas fa-save me-2"></i>
                    {{ isLoading ? 'Zapisywanie...' : (isEditing ? 'Aktualizuj kampanię' : 'Utwórz kampanię') }}
                  </button>

                  <router-link
                    to="/dashboard"
                    class="btn btn-outline-secondary btn-lg px-4"
                  >
                    <i class="fas fa-times me-2"></i>
                    Anuluj
                  </router-link>
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
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCampaignsStore } from '../stores/campaigns'
import type { Campaign, CompensationType } from '../types'

const route = useRoute()
const router = useRouter()
const campaignsStore = useCampaignsStore()

const isEditing = computed(() => !!route.params.id)
const campaignId = computed(() => route.params.id ? Number(route.params.id) : null)

const isLoading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

const form = reactive({
  title: '',
  description: '',
  category: '',
  media_channel: '',
  location: '',
  compensation: '' as CompensationType,
  budget_min: null as number | null,
  budget_max: null as number | null,
  barter_descr: '',
  deadline: ''
})

const showBudgetFields = computed(() => {
  return form.compensation === 'Cash' || form.compensation === 'Mixed'
})

const showBarterField = computed(() => {
  return form.compensation === 'Barter' || form.compensation === 'Mixed'
})

const requiresBudget = computed(() => {
  return form.compensation === 'Cash' || form.compensation === 'Mixed'
})

const requiresBarter = computed(() => {
  return form.compensation === 'Barter' || form.compensation === 'Mixed'
})

// Load campaign data if editing
const loadCampaign = async () => {
  if (isEditing.value && campaignId.value) {
    try {
      const campaign = campaignsStore.campaigns.find(c => c.id === campaignId.value)
      if (campaign) {
        Object.assign(form, {
          title: campaign.title,
          description: campaign.description,
          category: campaign.category,
          media_channel: campaign.media_channel,
          location: campaign.location,
          compensation: campaign.compensation,
          budget_min: campaign.budget_min,
          budget_max: campaign.budget_max,
          barter_descr: campaign.barter_descr || '',
          deadline: campaign.deadline ? new Date(campaign.deadline).toISOString().slice(0, 16) : ''
        })
      }
    } catch (err) {
      error.value = 'Błąd ładowania danych kampanii'
    }
  }
}

// Clear budget/barter fields when compensation type changes
watch(() => form.compensation, (newType) => {
  if (newType !== 'Cash' && newType !== 'Mixed') {
    form.budget_min = null
    form.budget_max = null
  }
  if (newType !== 'Barter' && newType !== 'Mixed') {
    form.barter_descr = ''
  }
})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    error.value = null
    success.value = false

    // Validation
    if (requiresBudget.value && (!form.budget_min || !form.budget_max)) {
      error.value = 'Budżet jest wymagany dla tego typu wynagrodzenia'
      return
    }

    if (requiresBarter.value && !form.barter_descr.trim()) {
      error.value = 'Opis barteru jest wymagany dla tego typu wynagrodzenia'
      return
    }

    if (form.budget_min && form.budget_max && form.budget_min > form.budget_max) {
      error.value = 'Budżet minimalny nie może być większy od maksymalnego'
      return
    }

    const submitData = {
      ...form,
      deadline: new Date(form.deadline).toISOString()
    }

    if (isEditing.value && campaignId.value) {
      await campaignsStore.updateCampaign(campaignId.value, submitData)
    } else {
      await campaignsStore.createCampaign(submitData)
    }

    success.value = true

    // Redirect after success
    setTimeout(() => {
      router.push('/dashboard')
    }, 2000)

  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Błąd zapisywania kampanii'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadCampaign()
})
</script>

<style scoped>
.add-campaign-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.campaign-navigation {
  margin-bottom: 2rem;
}

.back-button {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 500;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.campaign-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.bg-gradient-primary {
  background: linear-gradient(135deg, var(--violet) 0%, #6B2FDB 100%);
  padding: 3rem 2rem 2rem;
}

.campaign-header-content {
  position: relative;
  z-index: 2;
}

.campaign-icon {
  display: flex;
  justify-content: center;
}

.icon-circle {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  backdrop-filter: blur(10px);
}

.campaign-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: -0.025em;
}

.campaign-close-btn {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.campaign-close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: rotate(90deg) scale(1.1);
}

.card-body {
  padding: 3rem;
  background: white;
}

.compensation-options {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.form-check {
  flex: 1;
  min-width: 150px;
}

.form-check-label {
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}

.form-check-input:checked + .form-check-label {
  background: rgba(125, 60, 255, 0.1);
  color: var(--violet);
}

.budget-section, .barter-section {
  padding: 1.5rem;
  background: rgba(125, 60, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(125, 60, 255, 0.1);
}

.form-control, .form-select {
  border-radius: 8px;
  border: 2px solid #e9ecef;
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: var(--violet);
  box-shadow: 0 0 0 0.2rem rgba(125, 60, 255, 0.15);
}

.btn-lg {
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--violet);
  border-color: var(--violet);
}

.btn-primary:hover {
  background: #6B2FDB;
  border-color: #6B2FDB;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(125, 60, 255, 0.3);
}
</style>