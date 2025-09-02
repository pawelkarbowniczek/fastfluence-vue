<template>
  <div class="card h-100 campaign-card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title">{{ campaign.title }}</h5>
        <span class="badge bg-primary">{{ campaign.media_channel }}</span>
      </div>

      <p class="card-text text-muted small">
        {{ campaign.description }}
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
              ({{ campaign.budget_min }} - {{ campaign.budget_max }} PLN)
            </span>
          </div>
          <div v-if="campaign.barter_descr" class="text-muted small">
            {{ campaign.barter_descr }}
          </div>
        </div>

        <div class="deadline-info mb-3">
          <small class="text-muted">Deadline:</small>
          <div class="fw-semibold">{{ formatDate(campaign.deadline) }}</div>
        </div>

        <div class="owner-info">
          <small class="text-muted">Reklamodawca:</small>
          <div class="fw-semibold">{{ campaign.owner.display_name }}</div>
        </div>
      </div>
    </div>

    <div class="card-footer bg-transparent">
      <div class="d-flex gap-2">
        <button
          @click="$emit('view-details', campaign)"
          class="btn btn-outline-primary btn-sm flex-fill"
        >
          Zobacz szczegóły
        </button>
        <button
          v-if="canApply"
          @click="$emit('apply', campaign)"
          class="btn btn-primary btn-sm flex-fill"
        >
          Aplikuj
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import type { Campaign } from '../types'

interface Props {
  campaign: Campaign
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'view-details': [campaign: Campaign]
  'apply': [campaign: Campaign]
}>()

const authStore = useAuthStore()

const canApply = computed(() => {
  return authStore.isCreator && authStore.user?.id !== props.campaign.owner_id
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pl-PL')
}
</script>

<style scoped>
.campaign-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.campaign-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.card-title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.campaign-details {
  font-size: 0.9rem;
}
</style>