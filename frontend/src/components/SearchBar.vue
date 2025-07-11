<template>
  <div class="search-bar">
    <div class="row row-cols-lg-auto g-3 align-items-center">
      <div class="col">
        <select v-model="filters.category" class="form-select">
          <option value="">Kategoria ▾</option>
          <option value="Moda">Moda</option>
          <option value="Technologia">Technologia</option>
          <option value="Kulinaria">Kulinaria</option>
          <option value="Fitness">Fitness</option>
          <option value="Podróże">Podróże</option>
          <option value="Lifestyle">Lifestyle</option>
        </select>
      </div>
      
      <div class="col">
        <select v-model="filters.media_channel" class="form-select">
          <option value="">Kanał mediowy ▾</option>
          <option value="Instagram">Instagram</option>
          <option value="TikTok">TikTok</option>
          <option value="YouTube">YouTube</option>
          <option value="Blog">Blog</option>
          <option value="Facebook">Facebook</option>
          <option value="LinkedIn">LinkedIn</option>
          <option value="Other">Inne</option>
        </select>
      </div>
      
      <div class="col">
        <input 
          v-model="filters.location" 
          type="text" 
          class="form-control" 
          placeholder="Lokalizacja ▾"
        >
      </div>
      
      <div class="col">
        <select v-model="filters.compensation" class="form-select">
          <option value="">Wynagrodzenie ▾</option>
          <option value="Cash">Gotówka</option>
          <option value="Barter">Barter</option>
          <option value="Mixed">Mieszane</option>
        </select>
      </div>
      
      <div class="col">
        <div class="range-container">
          <label class="form-label small">Budżet: {{ filters.min_budget || 0 }} - {{ filters.max_budget || 50000 }} PLN</label>
          <RangeSlider 
            v-model:min="filters.min_budget"
            v-model:max="filters.max_budget"
            :min="0"
            :max="50000"
            :step="500"
          />
        </div>
      </div>
      
      <div class="col">
        <button @click="handleSearch" class="btn btn-primary">
          Szukaj
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import RangeSlider from './RangeSlider.vue'
import type { CampaignFilters, CreatorFilters } from '../types'

interface Props {
  modelValue?: CampaignFilters | CreatorFilters
  type?: 'campaigns' | 'creators'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'campaigns'
})

const emit = defineEmits<{
  'update:modelValue': [filters: CampaignFilters | CreatorFilters]
  search: [filters: CampaignFilters | CreatorFilters]
}>()

const filters = reactive<CampaignFilters | CreatorFilters>({
  category: '',
  media_channel: undefined,
  location: '',
  compensation: undefined,
  min_budget: 0,
  max_budget: 50000,
  ...props.modelValue
})

watch(filters, (newFilters) => {
  emit('update:modelValue', { ...newFilters })
}, { deep: true })

const handleSearch = () => {
  emit('search', { ...filters })
}
</script>

<style scoped>
.range-container {
  min-width: 200px;
}
</style>