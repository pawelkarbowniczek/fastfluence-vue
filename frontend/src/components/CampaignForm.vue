<template>
  <form @submit.prevent="handleSubmit" class="campaign-form">
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
          >
        </div>
      </div>
    </div>
    
    <div class="mb-3">
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
            Mieszane
          </label>
        </div>
      </div>
    </div>
    
    <div v-if="showBudgetFields" class="row">
      <div class="col-md-6">
        <div class="mb-3">
          <label for="budget_min" class="form-label">Budżet minimalny (PLN)</label>
          <input 
            v-model.number="form.budget_min" 
            type="number" 
            class="form-control" 
            id="budget_min"
            min="0"
            :required="requiresBudget"
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
            :required="requiresBudget"
          >
        </div>
      </div>
    </div>
    
    <div v-if="showBarterField" class="mb-3">
      <label for="barter_descr" class="form-label">Opis barteru</label>
      <textarea 
        v-model="form.barter_descr" 
        class="form-control" 
        id="barter_descr"
        rows="3"
        :required="requiresBarter"
      ></textarea>
    </div>
    
    <div class="mb-3">
      <label for="deadline" class="form-label">Deadline</label>
      <input 
        v-model="form.deadline" 
        type="datetime-local" 
        class="form-control" 
        id="deadline"
        required
      >
    </div>
    
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div class="d-flex gap-2">
      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        {{ isLoading ? 'Zapisywanie...' : (isEditing ? 'Aktualizuj' : 'Utwórz kampanię') }}
      </button>
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        Anuluj
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { Campaign, CompensationType } from '../types'

interface Props {
  campaign?: Campaign
  isLoading?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: Partial<Campaign>]
  cancel: []
}>()

const error = ref<string | null>(null)
const isEditing = computed(() => !!props.campaign)

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

// Initialize form with campaign data if editing
if (props.campaign) {
  Object.assign(form, {
    title: props.campaign.title,
    description: props.campaign.description,
    category: props.campaign.category,
    media_channel: props.campaign.media_channel,
    location: props.campaign.location,
    compensation: props.campaign.compensation,
    budget_min: props.campaign.budget_min,
    budget_max: props.campaign.budget_max,
    barter_descr: props.campaign.barter_descr,
    deadline: props.campaign.deadline ? new Date(props.campaign.deadline).toISOString().slice(0, 16) : ''
  })
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

const handleSubmit = () => {
  error.value = null
  
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
  
  emit('submit', submitData)
}
</script>

<style scoped>
.compensation-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.campaign-form {
  max-width: 800px;
}
</style>