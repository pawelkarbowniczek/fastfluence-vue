<template>
  <div class="dashboard">
    <div class="container py-4">
      <!-- Hero section with gradient background -->
      <div class="dashboard-hero text-center text-white mb-4">
        <div class="hero-content">
          <div class="hero-avatar mb-3">
            <div class="avatar-circle">
              {{ user?.display_name?.charAt(0)?.toUpperCase() || 'U' }}
            </div>
          </div>
          <h1 class="hero-title mb-2">
            {{ isAdvertiser ? 'Panel Reklamodawcy' : 'Znajdź zlecenie' }}
          </h1>
          <p class="hero-subtitle mb-0 opacity-75">
            {{ isAdvertiser
              ? 'Zarządzaj kampaniami i znajdź najlepszych twórców'
              : 'Odkryj najbardziej interesujące kampanie marketingowe'
            }}
          </p>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="search-section mb-4">
        <SearchBar
          v-model="filters"
          :type="isAdvertiser ? 'creators' : 'campaigns'"
          @search="handleSearch"
        />
      </div>

      <!-- Main Content Cards -->
      <div class="row g-4">
        <!-- Campaigns Section -->
        <div class="col-12">
          <div class="content-card">
            <div class="card-header-custom">
              <div class="d-flex justify-content-between align-items-center">
                <div class="header-info">
                  <h3 class="section-title mb-1">
                    <i class="fas fa-bullhorn me-2 text-primary"></i>
                    {{ isAdvertiser ? 'Moje kampanie' : 'Dostępne kampanie' }}
                  </h3>
                  <p class="section-subtitle mb-0 text-muted">
                    {{ isAdvertiser
                      ? `Zarządzaj swoimi ${myCampaigns.length} kampaniami`
                      : `Przeglądaj ${campaigns.length} dostępnych kampanii`
                    }}
                  </p>
                </div>
                <router-link
                  v-if="isAdvertiser"
                  to="/campaigns/add"
                  class="btn btn-primary btn-gradient"
                >
                  <i class="fas fa-plus me-2"></i>
                  Dodaj kampanię
                </router-link>
              </div>
            </div>

            <div class="card-body-custom">
              <div v-if="isAdvertiser" class="advertiser-view">
                <!-- Advertiser campaigns with applications -->
                <div v-if="myCampaigns.length > 0">
                  <div v-for="campaign in myCampaigns" :key="campaign.id" class="campaign-with-apps mb-4">
                    <div class="campaign-header">
                      <h5>{{ campaign.title }}</h5>
                      <span class="badge bg-primary">{{ campaign.media_channel }}</span>
                    </div>

                    <!-- Applications for this campaign -->
                    <div class="applications-section mt-3">
                      <h6 class="text-muted">Aplikacje ({{ getCampaignApplications(campaign.id).length }})</h6>

                      <div v-if="getCampaignApplications(campaign.id).length > 0" class="applications-list">
                        <div
                          v-for="application in getCampaignApplications(campaign.id)"
                          :key="application.id"
                          class="application-card"
                        >
                          <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                              <div class="d-flex align-items-center mb-2">
                                <strong>{{ application.creator.display_name }}</strong>
                                <span
                                  class="badge ms-2"
                                  :class="getStatusBadgeClass(application.status)"
                                >
                                  {{ getStatusText(application.status) }}
                                </span>
                              </div>

                              <p class="text-muted mb-2">{{ application.pitch_text }}</p>

                              <div v-if="application.proposed_price" class="text-success small">
                                <i class="fas fa-coins me-1"></i>
                                Proponowana cena: {{ application.proposed_price.toLocaleString('pl-PL') }} PLN
                              </div>

                              <small class="text-muted">
                                {{ formatDate(application.created_at) }}
                              </small>
                            </div>

                            <div v-if="application.status === 'pending'" class="application-actions">
                              <button
                                @click="updateApplicationStatus(application.id, 'accepted')"
                                class="btn btn-sm btn-success me-2"
                                :disabled="isUpdatingStatus"
                              >
                                Akceptuj
                              </button>
                              <button
                                @click="updateApplicationStatus(application.id, 'rejected')"
                                class="btn btn-sm btn-danger"
                                :disabled="isUpdatingStatus"
                              >
                                Odrzuć
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div v-else class="text-muted text-center py-3">
                        <i class="fas fa-inbox fa-2x mb-2"></i>
                        <p>Brak aplikacji na tę kampanię</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-else class="empty-state">
                  <div class="empty-icon">
                    <i class="fas fa-bullhorn fa-3x text-muted"></i>
                  </div>
                  <h5 class="text-muted">Nie masz jeszcze żadnych kampanii</h5>
                  <p class="text-muted">Utwórz swoją pierwszą kampanię, aby znaleźć idealnych twórców.</p>
                  <router-link to="/campaigns/add" class="btn btn-primary btn-gradient">
                    <i class="fas fa-plus me-2"></i>
                    Utwórz pierwszą kampanię
                  </router-link>
                </div>
              </div>

              <div v-else class="creator-view">
                <!-- Creator campaigns view -->
                <div v-if="campaigns.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                  <div v-for="campaign in campaigns" :key="campaign.id" class="col">
                    <CampaignCard
                      :campaign="campaign"
                      class="campaign-card-enhanced"
                      @view-details="showCampaignDetails"
                      @apply="showCampaignDetails"
                    />
                  </div>
                </div>

                <div v-else class="empty-state">
                  <div class="empty-icon">
                    <i class="fas fa-search fa-3x text-muted"></i>
                  </div>
                  <h5 class="text-muted">Nie znaleziono kampanii</h5>
                  <p class="text-muted">Spróbuj zmienić filtry wyszukiwania lub sprawdź później.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Campaign Details Modal -->
    <CampaignDetails
      v-if="selectedCampaign"
      :campaign="selectedCampaign"
      @close="selectedCampaign = null"
      @applied="handleApplicationSubmitted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCampaignsStore } from '../stores/campaigns'
import { applicationApi } from '../services/api'
import SearchBar from '../components/SearchBar.vue'
import CampaignCard from '../components/CampaignCard.vue'
import CampaignDetails from '../views/CampaignDetails.vue'
import type { CampaignFilters, CreatorFilters, Campaign, Application } from '../types'

const authStore = useAuthStore()
const campaignsStore = useCampaignsStore()

const isAdvertiser = computed(() => authStore.isAdvertiser)
const user = computed(() => authStore.user)
const campaigns = computed(() => campaignsStore.campaigns)

const myCampaigns = computed(() => {
  if (!authStore.user) return []
  return campaigns.value.filter(c => c.owner_id === authStore.user!.id)
})

const filters = ref<CampaignFilters | CreatorFilters>({})
const applications = ref<Application[]>([])
const selectedCampaign = ref<Campaign | null>(null)
const isUpdatingStatus = ref(false)

const getCampaignApplications = (campaignId: number) => {
  return applications.value.filter(app => app.campaign_id === campaignId)
}

const getStatusBadgeClass = (status: string) => {
  switch (status) {
    case 'accepted': return 'bg-success'
    case 'rejected': return 'bg-danger'
    default: return 'bg-warning'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'accepted': return 'Zaakceptowana'
    case 'rejected': return 'Odrzucona'
    default: return 'Oczekująca'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pl-PL')
}

const showCampaignDetails = (campaign: Campaign) => {
  selectedCampaign.value = campaign
}

const handleApplicationSubmitted = () => {
  loadApplications()
}

const updateApplicationStatus = async (applicationId: number, status: string) => {
  try {
    isUpdatingStatus.value = true
    await applicationApi.updateApplicationStatus(applicationId, status)
    await loadApplications()
  } catch (error) {
    console.error('Error updating application status:', error)
  } finally {
    isUpdatingStatus.value = false
  }
}

const handleSearch = async (searchFilters: CampaignFilters | CreatorFilters) => {
  if (!isAdvertiser.value) {
    await campaignsStore.fetchCampaigns(searchFilters as CampaignFilters)
  }
}

const loadApplications = async () => {
  if (isAdvertiser.value) {
    try {
      applications.value = await applicationApi.getApplications()
    } catch (error) {
      console.error('Error loading applications:', error)
    }
  }
}

const loadData = async () => {
  try {
    await campaignsStore.fetchCampaigns()
    if (isAdvertiser.value) {
      await loadApplications()
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>