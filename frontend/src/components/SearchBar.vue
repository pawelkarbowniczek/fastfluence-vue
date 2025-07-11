<template>
  <div class="search-bar">
    <div class="filter-header">
      <h2 class="filter-title">PRZEGLĄDAJ ZLECENIE <span class="highlight">WEDŁUG KATEGORII</span></h2>
    </div>

    <div class="filter-container">
      <div class="filter-row">
        <div class="filter-item">
          <select v-model="filters.category" class="filter-select">
            <option value="">Kategoria ▾</option>
            <option value="Moda">Moda</option>
            <option value="Technologia">Technologia</option>
            <option value="Kulinaria">Kulinaria</option>
            <option value="Fitness">Fitness</option>
            <option value="Podróże">Podróże</option>
            <option value="Lifestyle">Lifestyle</option>
          </select>
        </div>

        <div class="filter-item">
          <select v-model="filters.media_channel" class="filter-select">
            <option value="">Media Społecznościowe ▾</option>
            <option value="Instagram">Instagram</option>
            <option value="TikTok">TikTok</option>
            <option value="YouTube">YouTube</option>
            <option value="Blog">Blog</option>
            <option value="Facebook">Facebook</option>
            <option value="LinkedIn">LinkedIn</option>
            <option value="Other">Inne</option>
          </select>
        </div>

        <div class="filter-item">
          <select v-model="filters.location" class="filter-select">
            <option value="">Lokalizacja ▾</option>
            <option value="Warszawa">Warszawa</option>
            <option value="Kraków">Kraków</option>
            <option value="Gdańsk">Gdańsk</option>
            <option value="Poznań">Poznań</option>
            <option value="Wrocław">Wrocław</option>
            <option value="Łódź">Łódź</option>
            <option value="Cała Polska">Cała Polska</option>
          </select>
        </div>

        <div class="filter-item">
          <select v-model="filters.compensation" class="filter-select">
            <option value="">Cena ▾</option>
            <option value="Cash">Gotówka</option>
            <option value="Barter">Barter</option>
            <option value="Mixed">Mieszane</option>
          </select>
        </div>

        <div class="filter-item find-button">
          <button @click="handleSearch" class="btn-find">
            ZNAJDŹ
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
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
.search-bar {
  background: white;
  padding: 3rem 2rem;
  margin-bottom: 3rem;
}

.filter-header {
  text-align: center;
  margin-bottom: 3rem;
}

.filter-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #2c3e50;
  letter-spacing: -0.02em;
  margin: 0;
  line-height: 1.2;
}

.highlight {
  color: var(--violet);
}

.filter-container {
  max-width: 1000px;
  margin: 0 auto;
}

.filter-row {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.filter-item {
  flex: 0 0 auto;
}

.filter-select {
  min-width: 200px;
  padding: 14px 20px;
  border: 2px solid #ddd;
  border-radius: 8px;
  background: white;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 12px center;
  background-repeat: no-repeat;
  background-size: 16px;
  padding-right: 40px;
}

.filter-select:hover {
  border-color: var(--violet);
  box-shadow: 0 0 0 1px var(--violet);
}

.filter-select:focus {
  outline: none;
  border-color: var(--violet);
  box-shadow: 0 0 0 3px rgba(125, 60, 255, 0.1);
}

.find-button {
  margin-left: 1rem;
}

.btn-find {
  background: var(--violet);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 14px 40px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.5px;
  min-width: 120px;
}

.btn-find:hover {
  background: #6B2FDB;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(125, 60, 255, 0.3);
}

.btn-find:active {
  transform: translateY(0);
}

@media (max-width: 1200px) {
  .filter-row {
    justify-content: flex-start;
  }

  .filter-select {
    min-width: 180px;
  }
}

@media (max-width: 768px) {
  .search-bar {
    padding: 2rem 1rem;
  }

  .filter-title {
    font-size: 1.8rem;
  }

  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .filter-item {
    width: 100%;
  }

  .filter-select {
    min-width: 100%;
  }

  .find-button {
    margin-left: 0;
    margin-top: 1rem;
  }

  .btn-find {
    width: 100%;
  }
}
</style>