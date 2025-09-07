<template>
  <div class="card h-100 campaign-card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title">{{ campaign.title }}</h5>
        <span class="badge bg-primary">{{ campaign.media_channel }}</span>
      </div>

      <p class="card-text text-muted small">
        {{ truncateDescription(campaign.description) }}
      </p>

      <div class="campaign-details">
        <div class="row g-2 mb-3">
          <div class="col-6">
            <small class="text-muted">Kategoria:</small>
            <div class="fw-semibold">{{ campaign.category }}</div>
          </div>
          <div class="col-6">
            <small class="text-muted">Lokalizacja:</small>
            <div class="fw-semibold">{{ campaign.location }}</div>
          </div>
        </div>

        <div class="compensation-info mb-3">
          <small class="text-muted">Wynagrodzenie:</small>
          <div class="fw-semibold">
            {{ campaign.compensation }}
            <span v-if="campaign.budget_min && campaign.budget_max" class="text-success">
              ({{ formatCurrency(campaign.budget_min) }} - {{ formatCurrency(campaign.budget_max) }})
            </span>
          </div>
          <div v-if="campaign.barter_descr" class="text-muted small">
            {{ truncateText(campaign.barter_descr, 50) }}
          </div>
        </div>

        <div class="deadline-info mb-3">
          <small class="text-muted">Deadline:</small>
          <div class="fw-semibold" :class="getDeadlineClass(campaign.deadline)">
            {{ formatDate(campaign.deadline) }}
            <small class="d-block">{{ getTimeLeft(campaign.deadline) }}</small>
          </div>
        </div>

        <div class="owner-info">
          <small class="text-muted">Reklamodawca:</small>
          <div class="fw-semibold">{{ campaign.owner.display_name }}</div>
        </div>
      </div>
    </div>

    <div class="card-footer bg-transparent">
      <div class="d-flex gap-2">
        <router-link
          :to="`/campaigns/${campaign.id}`"
          class="btn btn-outline-primary btn-sm flex-fill"
        >
          <i class="fas fa-eye me-1"></i>
          Zobacz szczegóły
        </router-link>
        <button
          v-if="canApply"
          @click="goToCampaignDetails"
          class="btn btn-primary btn-sm flex-fill"
        >
          <i class="fas fa-paper-plane me-1"></i>
          Aplikuj
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import type { Campaign } from '../types'

interface Props {
  campaign: Campaign
}

const props = defineProps<Props>()
const router = useRouter()
const authStore = useAuthStore()

const canApply = computed(() => {
  return authStore.isCreator && authStore.user?.id !== props.campaign.owner_id
})

const goToCampaignDetails = () => {
  router.push(`/campaigns/${props.campaign.id}`)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
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

const truncateDescription = (text: string) => {
  if (text.length <= 100) return text
  return text.substring(0, 100) + '...'
}

const truncateText = (text: string, maxLength: number) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<style scoped>
.campaign-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: none;
  border-radius: 15px;
  overflow: hidden;
}

.campaign-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.card-title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--violet);
  font-weight: 600;
}

.campaign-details {
  font-size: 0.9rem;
}

.card-footer {
  border-top: 1px solid rgba(0,0,0,0.1);
  padding: 1rem;
}

.btn-sm {
  border-radius: 8px;
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.btn-outline-primary {
  border-color: var(--violet);
  color: var(--violet);
}

.btn-outline-primary:hover {
  background-color: var(--violet);
  border-color: var(--violet);
  color: white;
  transform: translateY(-1px);
}

.btn-primary {
  background-color: var(--violet);
  border-color: var(--violet);
}

.btn-primary:hover {
  background-color: #6B2FDB;
  border-color: #6B2FDB;
  transform: translateY(-1px);
}

.compensation-info,
.deadline-info,
.owner-info {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.compensation-info:last-child,
.deadline-info:last-child,
.owner-info:last-child {
  border-bottom: none;
}
</style>