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
        <!-- My Campaigns / Available Campaigns -->
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
                <div v-if="myCampaigns.length > 0">
                  <TableBase
                    :data="myCampaigns"
                    :columns="campaignColumns"
                    class="custom-table"
                  >
                    <template #cell-title="{ item }">
                      <div class="campaign-title">
                        <strong>{{ item.title }}</strong>
                        <small class="text-muted d-block">{{ item.category }}</small>
                      </div>
                    </template>
                    <template #cell-compensation="{ item }">
                      <span class="badge badge-custom" :class="getCompensationClass(item.compensation)">
                        {{ item.compensation }}
                      </span>
                      <span v-if="item.budget_min && item.budget_max" class="text-muted small d-block">
                        {{ formatCurrency(item.budget_min) }} - {{ formatCurrency(item.budget_max) }}
                      </span>
                    </template>
                    <template #cell-deadline="{ item }">
                      <div class="deadline-info">
                        {{ formatDate(item.deadline) }}
                        <small class="text-muted d-block">{{ getTimeLeft(item.deadline) }}</small>
                      </div>
                    </template>
                    <template #actions="{ item }">
                      <div class="action-buttons">
                        <router-link
                          :to="`/campaigns/edit/${item.id}`"
                          class="btn btn-sm btn-outline-primary me-2"
                        >
                          <i class="fas fa-edit me-1"></i>
                          Edytuj
                        </router-link>
                        <button
                          @click="deleteCampaign(item.id)"
                          class="btn btn-sm btn-outline-danger"
                        >
                          <i class="fas fa-trash me-1"></i>
                          Usuń
                        </button>
                      </div>
                    </template>
                  </TableBase>
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
                <div v-if="campaigns.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                  <div v-for="campaign in campaigns" :key="campaign.id" class="col">
                    <CampaignCard :campaign="campaign" class="campaign-card-enhanced" />
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

        <!-- Creators Section (for advertisers) -->
        <div v-if="isAdvertiser" class="col-12">
          <div class="content-card">
            <div class="card-header-custom">
              <div class="header-info">
                <h3 class="section-title mb-1">
                  <i class="fas fa-users me-2 text-success"></i>
                  Szukaj twórców
                </h3>
                <p class="section-subtitle mb-0 text-muted">
                  Znajdź idealnych partnerów do współpracy
                </p>
              </div>
            </div>

            <div class="card-body-custom">
              <div v-if="creators.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                <div v-for="creator in creators" :key="creator.id" class="col">
                  <CreatorCard :creator="creator" class="creator-card-enhanced" />
                </div>
              </div>
              <div v-else class="empty-state">
                <div class="empty-icon">
                  <i class="fas fa-user-friends fa-3x text-muted"></i>
                </div>
                <h5 class="text-muted">Nie znaleziono twórców</h5>
                <p class="text-muted">Spróbuj zmienić filtry wyszukiwania.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCampaignsStore } from '../stores/campaigns'
import SearchBar from '../components/SearchBar.vue'
import CreatorCard from '../components/CreatorCard.vue'
import CampaignCard from '../components/CampaignCard.vue'
import TableBase from '../components/TableBase.vue'
import type { CampaignFilters, CreatorFilters } from '../types'

const authStore = useAuthStore()
const campaignsStore = useCampaignsStore()

const isAdvertiser = computed(() => authStore.isAdvertiser)
const user = computed(() => authStore.user)
const filters = ref<CampaignFilters | CreatorFilters>({})

const campaigns = computed(() => campaignsStore.campaigns)
const creators = computed(() => campaignsStore.creators)

const myCampaigns = computed(() => {
  if (!authStore.user) return []
  return campaigns.value.filter(c => c.owner_id === authStore.user!.id)
})

const campaignColumns = [
  { key: 'title', label: 'Kampania', sortable: true },
  { key: 'media_channel', label: 'Kanał', sortable: true },
  { key: 'compensation', label: 'Wynagrodzenie' },
  { key: 'deadline', label: 'Deadline', sortable: true, type: 'date' }
]

const handleSearch = async (searchFilters: CampaignFilters | CreatorFilters) => {
  if (isAdvertiser.value) {
    await campaignsStore.fetchCreators(searchFilters as CreatorFilters)
  } else {
    await campaignsStore.fetchCampaigns(searchFilters as CampaignFilters)
  }
}

const deleteCampaign = async (campaignId: number) => {
  if (confirm('Czy na pewno chcesz usunąć tę kampanię?')) {
    try {
      await campaignsStore.deleteCampaign(campaignId)
    } catch (error) {
      console.error('Error deleting campaign:', error)
    }
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pl-PL')
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

const getCompensationClass = (compensation: string) => {
  switch (compensation) {
    case 'Cash': return 'badge-success'
    case 'Barter': return 'badge-info'
    case 'Mixed': return 'badge-warning'
    default: return 'badge-secondary'
  }
}

const loadData = async () => {
  try {
    if (isAdvertiser.value) {
      await campaignsStore.fetchCampaigns()
      await campaignsStore.fetchCreators()
    } else {
      await campaignsStore.fetchCampaigns()
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.dashboard-hero {
  padding: 3rem 2rem;
  margin-bottom: 2rem;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-avatar {
  display: flex;
  justify-content: center;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
  backdrop-filter: blur(10px);
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  letter-spacing: -0.025em;
}

.hero-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
}

.search-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.content-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20px);
  border: none;
}

.card-header-custom {
  background: linear-gradient(135deg, rgba(125, 60, 255, 0.1) 0%, rgba(212, 255, 50, 0.1) 100%);
  padding: 2rem;
  border-bottom: 1px solid rgba(125, 60, 255, 0.1);
}

.header-info h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.section-subtitle {
  font-size: 0.95rem;
}

.card-body-custom {
  padding: 2rem;
}

.btn-gradient {
  background: linear-gradient(135deg, var(--violet) 0%, #6B2FDB 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(125, 60, 255, 0.3);
  color: white;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.badge-custom {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 500;
}

.badge-success {
  background-color: #d1e7dd;
  color: #0f5132;
}

.badge-info {
  background-color: #cff4fc;
  color: #055160;
}

.badge-warning {
  background-color: #fff3cd;
  color: #664d03;
}

.campaign-title strong {
  font-size: 1rem;
  color: #2c3e50;
}

.deadline-info {
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  border-radius: 6px;
  font-weight: 500;
}

.btn-outline-primary {
  border-color: var(--violet);
  color: var(--violet);
}

.btn-outline-primary:hover {
  background-color: var(--violet);
  border-color: var(--violet);
}

.campaign-card-enhanced,
.creator-card-enhanced {
  transition: all 0.3s ease;
}

.campaign-card-enhanced:hover,
.creator-card-enhanced:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.custom-table {
  border-radius: 12px;
  overflow: hidden;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .avatar-circle {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }

  .card-header-custom,
  .card-body-custom {
    padding: 1.5rem;
  }
}
</style>