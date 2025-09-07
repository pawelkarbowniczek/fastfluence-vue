<template>
  <div class="campaign-details-page">
    <div class="container py-4">
      <!-- Navigation breadcrumb -->
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

      <div v-if="campaign" class="row justify-content-center">
        <div class="col-lg-8">
          <!-- Campaign Header Card -->
          <div class="card shadow-lg campaign-header-card mb-4">
            <div class="card-header bg-gradient-primary text-white position-relative">
              <div class="campaign-header-content">
                <div class="d-flex align-items-center mb-3">
                  <div class="campaign-icon me-3">
                    <div class="icon-circle">
                      <i class="fas fa-bullhorn fa-2x"></i>
                    </div>
                  </div>
                  <div>
                    <h1 class="campaign-title mb-0">{{ campaign.title }}</h1>
                    <p class="mb-0 opacity-75">{{ campaign.category }}</p>
                  </div>
                </div>

                <div class="campaign-badges">
                  <span class="badge badge-custom me-2">
                    <i class="fas fa-hashtag me-1"></i>
                    {{ campaign.media_channel }}
                  </span>
                  <span class="badge badge-custom me-2">
                    <i class="fas fa-map-marker-alt me-1"></i>
                    {{ campaign.location }}
                  </span>
                  <span class="badge badge-custom" :class="getCompensationClass(campaign.compensation)">
                    <i class="fas fa-coins me-1"></i>
                    {{ campaign.compensation }}
                  </span>
                </div>
              </div>

              <router-link
                to="/dashboard"
                class="campaign-close-btn"
                title="Zamknij"
              >
                <i class="fas fa-times"></i>
              </router-link>
            </div>
          </div>

          <!-- Campaign Content -->
          <div class="row g-4">
            <!-- Main Details -->
            <div class="col-md-8">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <h3 class="card-title text-primary mb-3">
                    <i class="fas fa-info-circle me-2"></i>
                    Opis kampanii
                  </h3>
                  <p class="card-text fs-6 lh-lg">{{ campaign.description }}</p>

                  <!-- Compensation Details -->
                  <div class="compensation-section mt-4">
                    <h4 class="text-primary mb-3">
                      <i class="fas fa-money-bill-wave me-2"></i>
                      Wynagrodzenie
                    </h4>

                    <div class="compensation-details">
                      <div class="compensation-type mb-3">
                        <span class="badge badge-lg" :class="getCompensationClass(campaign.compensation)">
                          {{ getCompensationLabel(campaign.compensation) }}
                        </span>
                      </div>

                      <div v-if="campaign.budget_min && campaign.budget_max" class="budget-info mb-3">
                        <div class="budget-range">
                          <div class="budget-item">
                            <span class="text-muted small">Budżet minimalny</span>
                            <div class="budget-value text-success fw-bold">
                              {{ formatCurrency(campaign.budget_min) }}
                            </div>
                          </div>
                          <div class="budget-separator">-</div>
                          <div class="budget-item">
                            <span class="text-muted small">Budżet maksymalny</span>
                            <div class="budget-value text-success fw-bold">
                              {{ formatCurrency(campaign.budget_max) }}
                            </div>
                          </div>
                        </div>
                      </div>

                      <div v-if="campaign.barter_descr" class="barter-info">
                        <h6 class="text-muted mb-2">Szczegóły barteru:</h6>
                        <p class="barter-description">{{ campaign.barter_descr }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Application Section (for creators) -->
                  <div v-if="canApply" class="application-section mt-4">
                    <h4 class="text-primary mb-3">
                      <i class="fas fa-paper-plane me-2"></i>
                      Aplikuj na kampanię
                    </h4>

                    <div v-if="!showApplicationForm" class="text-center">
                      <button
                        @click="showApplicationForm = true"
                        class="btn btn-primary-gradient btn-lg px-4"
                      >
                        <i class="fas fa-plus me-2"></i>
                        Wyślij aplikację
                      </button>
                    </div>

                    <div v-else class="application-form">
                      <form @submit.prevent="submitApplication">
                        <div class="mb-3">
                          <label for="pitch" class="form-label fw-semibold">
                            Twoja propozycja <span class="text-danger">*</span>
                          </label>
                          <textarea
                            v-model="applicationForm.pitch_text"
                            id="pitch"
                            class="form-control form-control-custom"
                            rows="4"
                            placeholder="Opisz dlaczego jesteś idealnym kandydatem do tej kampanii..."
                            required
                          ></textarea>
                        </div>

                        <div v-if="campaign.compensation === 'Cash' || campaign.compensation === 'Mixed'" class="mb-3">
                          <label for="price" class="form-label fw-semibold">
                            Proponowana cena (PLN)
                          </label>
                          <input
                            v-model.number="applicationForm.proposed_price"
                            type="number"
                            id="price"
                            class="form-control form-control-custom"
                            min="0"
                            step="100"
                            placeholder="Wprowadź swoją cenę"
                          >
                        </div>

                        <div v-if="applicationError" class="alert alert-danger">
                          <i class="fas fa-exclamation-triangle me-2"></i>
                          {{ applicationError }}
                        </div>

                        <div class="d-flex gap-2">
                          <button
                            type="submit"
                            class="btn btn-primary-gradient"
                            :disabled="isSubmittingApplication"
                          >
                            <i class="fas fa-paper-plane me-2"></i>
                            {{ isSubmittingApplication ? 'Wysyłanie...' : 'Wyślij aplikację' }}
                          </button>
                          <button
                            type="button"
                            @click="showApplicationForm = false"
                            class="btn btn-outline-secondary"
                          >
                            <i class="fas fa-times me-2"></i>
                            Anuluj
                          </button>
                        </div>
                      </form>
                    </div>

                    <div v-if="applicationSuccess" class="alert alert-success mt-3">
                      <i class="fas fa-check-circle me-2"></i>
                      Aplikacja została wysłana pomyślnie!
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sidebar -->
            <div class="col-md-4">
              <div class="card shadow-sm sticky-top">
                <div class="card-body">
                  <!-- Campaign Owner -->
                  <div class="owner-section mb-4">
                    <h5 class="card-title text-primary mb-3">
                      <i class="fas fa-user me-2"></i>
                      Reklamodawca
                    </h5>
                    <div class="owner-info">
                      <div class="d-flex align-items-center mb-2">
                        <div class="owner-avatar me-3">
                          {{ campaign.owner.display_name.charAt(0).toUpperCase() }}
                        </div>
                        <div>
                          <div class="fw-bold">{{ campaign.owner.display_name }}</div>
                          <small class="text-muted">{{ campaign.owner.contact_email }}</small>
                        </div>
                      </div>

                      <div v-if="campaign.owner.website_url" class="mt-2">
                        <a :href="campaign.owner.website_url" target="_blank" class="text-decoration-none">
                          <i class="fas fa-globe me-1"></i>
                          Strona internetowa
                        </a>
                      </div>
                    </div>
                  </div>

                  <!-- Campaign Stats -->
                  <div class="stats-section mb-4">
                    <h5 class="card-title text-primary mb-3">
                      <i class="fas fa-chart-bar me-2"></i>
                      Informacje
                    </h5>

                    <div class="stat-item">
                      <div class="stat-label">Data utworzenia</div>
                      <div class="stat-value">{{ formatDate(campaign.created_at) }}</div>
                    </div>

                    <div class="stat-item">
                      <div class="stat-label">Deadline</div>
                      <div class="stat-value" :class="getDeadlineClass(campaign.deadline)">
                        {{ formatDate(campaign.deadline) }}
                        <small class="d-block">{{ getTimeLeft(campaign.deadline) }}</small>
                      </div>
                    </div>
                  </div>

                  <!-- Action Buttons -->
                  <div class="action-buttons">
                    <div v-if="canApply" class="d-grid gap-2">
                      <button
                        v-if="!showApplicationForm"
                        @click="showApplicationForm = true"
                        class="btn btn-primary-gradient"
                      >
                        <i class="fas fa-paper-plane me-2"></i>
                        Aplikuj teraz
                      </button>
                    </div>

                    <div v-else-if="isOwner" class="d-grid gap-2">
                      <router-link
                        :to="`/campaigns/edit/${campaign.id}`"
                        class="btn btn-outline-primary"
                      >
                        <i class="fas fa-edit me-2"></i>
                        Edytuj kampanię
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3" role="status">
          <span class="visually-hidden">Ładowanie...</span>
        </div>
        <h4>Ładowanie szczegółów kampanii...</h4>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-5">
        <div class="error-icon mb-3">
          <i class="fas fa-exclamation-triangle fa-4x text-danger"></i>
        </div>
        <h4 class="text-danger">Kampania nie została znaleziona</h4>
        <p class="text-muted">Kampania mogła zostać usunięta lub nie masz uprawnień do jej wyświetlenia.</p>
        <router-link to="/dashboard" class="btn btn-primary">
          Powrót do Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { campaignApi, applicationApi } from '../services/api'
import type { Campaign } from '../types'

const route = useRoute()
const authStore = useAuthStore()

const campaign = ref<Campaign | null>(null)
const isLoading = ref(true)
const showApplicationForm = ref(false)
const isSubmittingApplication = ref(false)
const applicationError = ref<string | null>(null)
const applicationSuccess = ref(false)

const applicationForm = ref({
  pitch_text: '',
  proposed_price: null as number | null
})

const campaignId = computed(() => Number(route.params.id))
const isOwner = computed(() => campaign.value?.owner_id === authStore.user?.id)
const canApply = computed(() =>
  authStore.isCreator &&
  campaign.value &&
  campaign.value.owner_id !== authStore.user?.id
)

const loadCampaign = async () => {
  try {
    isLoading.value = true
    campaign.value = await campaignApi.getCampaign(campaignId.value)
  } catch (error) {
    console.error('Error loading campaign:', error)
    campaign.value = null
  } finally {
    isLoading.value = false
  }
}

const submitApplication = async () => {
  if (!campaign.value) return

  try {
    isSubmittingApplication.value = true
    applicationError.value = null

    await applicationApi.createApplication({
      campaign_id: campaign.value.id,
      pitch_text: applicationForm.value.pitch_text,
      proposed_price: applicationForm.value.proposed_price
    })

    applicationSuccess.value = true
    showApplicationForm.value = false

    // Reset form
    applicationForm.value = {
      pitch_text: '',
      proposed_price: null
    }

  } catch (error: any) {
    applicationError.value = error.response?.data?.detail || 'Błąd wysyłania aplikacji'
  } finally {
    isSubmittingApplication.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pl-PL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatCurrency = (amount: number) => {
  return `${amount.toLocaleString('pl-PL')} PLN`
}

const getTimeLeft = (deadline: string) => {
  const now = new Date()
  const end = new Date(deadline)
  const diff = end.getTime() - now.getTime()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

  if (days < 0) return 'Wygasła'
  if (days === 0) return 'Dzisiaj'
  if (days === 1) return 'Jutro'
  return `${days} dni`
}

const getDeadlineClass = (deadline: string) => {
  const now = new Date()
  const end = new Date(deadline)
  const diff = end.getTime() - now.getTime()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

  if (days < 0) return 'text-danger'
  if (days <= 3) return 'text-warning'
  return 'text-success'
}

const getCompensationClass = (compensation: string) => {
  switch (compensation) {
    case 'Cash': return 'badge-success'
    case 'Barter': return 'badge-info'
    case 'Mixed': return 'badge-warning'
    default: return 'badge-secondary'
  }
}

const getCompensationLabel = (compensation: string) => {
  switch (compensation) {
    case 'Cash': return 'Gotówka'
    case 'Barter': return 'Barter'
    case 'Mixed': return 'Mieszane'
    default: return compensation
  }
}

onMounted(() => {
  loadCampaign()
})
</script>

<style scoped>
.campaign-details-page {
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

.campaign-header-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.bg-gradient-primary {
  background: linear-gradient(135deg, var(--violet) 0%, #6B2FDB 100%);
  padding: 2rem;
}

.campaign-header-content {
  position: relative;
  z-index: 2;
}

.campaign-icon .icon-circle {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
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

.campaign-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge-custom {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.badge-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 25px;
}

.badge-success {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border-color: rgba(40, 167, 69, 0.3);
}

.badge-info {
  background-color: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
  border-color: rgba(23, 162, 184, 0.3);
}

.badge-warning {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border-color: rgba(255, 193, 7, 0.3);
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

.compensation-section {
  background: rgba(125, 60, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(125, 60, 255, 0.1);
}

.budget-range {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.budget-item {
  flex: 1;
  text-align: center;
}

.budget-value {
  font-size: 1.25rem;
}

.budget-separator {
  font-size: 1.5rem;
  font-weight: bold;
  color: #6c757d;
}

.barter-description {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid var(--violet);
  margin: 0;
}

.owner-avatar {
  width: 50px;
  height: 50px;
  background: var(--violet);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
}

.stat-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #e9ecef;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-weight: 600;
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

.application-form {
  background: rgba(125, 60, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(125, 60, 255, 0.1);
}

.sticky-top {
  top: 1rem;
}

@media (max-width: 768px) {
  .campaign-details-page {
    padding: 1rem 0;
  }

  .bg-gradient-primary {
    padding: 1.5rem;
  }

  .campaign-title {
    font-size: 1.5rem;
  }

  .budget-range {
    flex-direction: column;
    gap: 0.5rem;
  }

  .budget-separator {
    transform: rotate(90deg);
  }
}
</style>