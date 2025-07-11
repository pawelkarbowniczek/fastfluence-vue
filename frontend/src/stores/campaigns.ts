import { defineStore } from 'pinia'
import { ref } from 'vue'
import { campaignApi, creatorApi } from '../services/api'
import type { Campaign, CampaignFilters, CreatorFilters, User } from '../types'

export const useCampaignsStore = defineStore('campaigns', () => {
  const campaigns = ref<Campaign[]>([])
  const creators = ref<User[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchCampaigns = async (filters?: CampaignFilters) => {
    try {
      isLoading.value = true
      error.value = null
      
      const data = await campaignApi.getCampaigns(filters)
      campaigns.value = data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd pobierania kampanii'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchCreators = async (filters?: CreatorFilters) => {
    try {
      isLoading.value = true
      error.value = null
      
      const data = await creatorApi.getCreators(filters)
      creators.value = data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd pobierania twórców'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createCampaign = async (campaignData: Partial<Campaign>) => {
    try {
      const newCampaign = await campaignApi.createCampaign(campaignData)
      campaigns.value.unshift(newCampaign)
      return newCampaign
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd tworzenia kampanii'
      throw err
    }
  }

  const updateCampaign = async (id: number, campaignData: Partial<Campaign>) => {
    try {
      const updatedCampaign = await campaignApi.updateCampaign(id, campaignData)
      const index = campaigns.value.findIndex(c => c.id === id)
      if (index !== -1) {
        campaigns.value[index] = updatedCampaign
      }
      return updatedCampaign
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd aktualizacji kampanii'
      throw err
    }
  }

  const deleteCampaign = async (id: number) => {
    try {
      await campaignApi.deleteCampaign(id)
      campaigns.value = campaigns.value.filter(c => c.id !== id)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Błąd usuwania kampanii'
      throw err
    }
  }

  return {
    campaigns,
    creators,
    isLoading,
    error,
    fetchCampaigns,
    fetchCreators,
    createCampaign,
    updateCampaign,
    deleteCampaign
  }
})