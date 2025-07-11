<template>
  <div class="dashboard">
    <div class="container-fluid py-4">
      <div class="row">
        <div class="col-12">
          <h1 class="mb-4">
            {{ isAdvertiser ? 'Panel Reklamodawcy' : 'Panel Influencera' }}
          </h1>
          
          <div class="row mb-4">
            <div class="col-md-8">
              <SearchBar 
                v-model="filters"
                :type="isAdvertiser ? 'creators' : 'campaigns'"
                @search="handleSearch"
              />
            </div>
            <div class="col-md-4 text-end">
              <button 
                v-if="isAdvertiser"
                @click="showCampaignForm = true"
                class="btn btn-primary"
              >
                Dodaj kampanię
              </button>
            </div>
          </div>
          
          <div class="row">
            <div class="col-12">
              <div v-if="isAdvertiser" class="advertiser-view">
                <div class="mb-4">
                  <h3>Moje kampanie</h3>
                  <TableBase 
                    :data="myCampaigns"
                    :columns="campaignColumns"
                  >
                    <template #cell-title="{ item }">
                      <strong>{{ item.title }}</strong>
                    </template>
                    <template #cell-compensation="{ item }">
                      <span class="badge bg-info">{{ item.compensation }}</span>
                      <span v-if="item.budget_min && item.budget_max" class="text-muted small d-block">
                        {{ item.budget_min }} - {{ item.budget_max }} PLN
                      </span>
                    </template>
                    <template #actions="{ item }">
                      <button @click="editCampaign(item)" class="btn btn-sm btn-outline-primary me-2">
                        Edytuj
                      </button>
                      <button @click="deleteCampaign(item.id)" class="btn btn-sm btn-outline-danger">
                        Usuń
                      </button>
                    </template>
                  </TableBase>
                </div>
                
                <div>
                  <h3>Szukaj twórców</h3>
                  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    <div v-for="creator in creators" :key="creator.id" class="col">
                      <CreatorCard :creator="creator" />
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-else class="creator-view">
                <div class="mb-4">
                  <h3>Dostępne kampanie</h3>
                  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    <div v-for="campaign in campaigns" :key="campaign.id" class="col">
                      <CampaignCard :campaign="campaign" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Campaign Form Modal -->
    <ModalBase v-if="showCampaignForm" @close="closeCampaignForm">
      <div class="modal-header">
        <h5 class="modal-title">
          {{ editingCampaign ? 'Edytuj kampanię' : 'Dodaj nową kampanię' }}
        </h5>
        <button type="button" class="btn-close" @click="closeCampaignForm"></button>
      </div>
      
      <div class="modal-body">
        <CampaignForm 
          :campaign="editingCampaign"
          :is-loading="isLoading"
          @submit="handleCampaignSubmit"
          @cancel="closeCampaignForm"
        />
      </div>
    </ModalBase>
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
import ModalBase from '../components/ModalBase.vue'
import CampaignForm from '../components/CampaignForm.vue'
import type { Campaign, CampaignFilters, CreatorFilters } from '../types'

const authStore = useAuthStore()
const campaignsStore = useCampaignsStore()

const isAdvertiser = computed(() => authStore.isAdvertiser)
const filters = ref<CampaignFilters | CreatorFilters>({})
const showCampaignForm = ref(false)
const editingCampaign = ref<Campaign | null>(null)
const isLoading = ref(false)

const campaigns = computed(() => campaignsStore.campaigns)
const creators = computed(() => campaignsStore.creators)

const myCampaigns = computed(() => {
  if (!authStore.user) return []
  return campaigns.value.filter(c => c.owner_id === authStore.user!.id)
})

const campaignColumns = [
  { key: 'title', label: 'Tytuł', sortable: true },
  { key: 'category', label: 'Kategoria', sortable: true },
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

const handleCampaignSubmit = async (data: Partial<Campaign>) => {
  try {
    isLoading.value = true
    
    if (editingCampaign.value) {
      await campaignsStore.updateCampaign(editingCampaign.value.id, data)
    } else {
      await campaignsStore.createCampaign(data)
    }
    
    closeCampaignForm()
    await loadData()
  } catch (error) {
    console.error('Error saving campaign:', error)
  } finally {
    isLoading.value = false
  }
}

const editCampaign = (campaign: Campaign) => {
  editingCampaign.value = campaign
  showCampaignForm.value = true
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

const closeCampaignForm = () => {
  showCampaignForm.value = false
  editingCampaign.value = null
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
  min-height: 80vh;
}

.advertiser-view, .creator-view {
  margin-top: 2rem;
}
</style>