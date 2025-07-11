<template>
  <div class="range-slider">
    <input
      type="range"
      :min="min"
      :max="max"
      :step="step"
      :value="minValue"
      @input="updateMin"
      class="range-input range-input-min"
    >
    <input
      type="range"
      :min="min"
      :max="max"
      :step="step"
      :value="maxValue"
      @input="updateMax"
      class="range-input range-input-max"
    >
    <div class="range-track">
      <div 
        class="range-progress"
        :style="progressStyle"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Props {
  min: number
  max: number
  step?: number
  minValue?: number
  maxValue?: number
}

const props = withDefaults(defineProps<Props>(), {
  step: 1,
  minValue: 0,
  maxValue: 100
})

const emit = defineEmits<{
  'update:min': [value: number]
  'update:max': [value: number]
}>()

const minValue = ref(props.minValue)
const maxValue = ref(props.maxValue)

const progressStyle = computed(() => {
  const minPercent = ((minValue.value - props.min) / (props.max - props.min)) * 100
  const maxPercent = ((maxValue.value - props.min) / (props.max - props.min)) * 100
  
  return {
    left: `${minPercent}%`,
    width: `${maxPercent - minPercent}%`
  }
})

const updateMin = (event: Event) => {
  const target = event.target as HTMLInputElement
  const value = parseInt(target.value)
  
  if (value <= maxValue.value) {
    minValue.value = value
    emit('update:min', value)
  }
}

const updateMax = (event: Event) => {
  const target = event.target as HTMLInputElement
  const value = parseInt(target.value)
  
  if (value >= minValue.value) {
    maxValue.value = value
    emit('update:max', value)
  }
}

watch(() => props.minValue, (newVal) => {
  minValue.value = newVal || 0
})

watch(() => props.maxValue, (newVal) => {
  maxValue.value = newVal || 100
})
</script>

<style scoped>
.range-slider {
  position: relative;
  width: 100%;
  height: 20px;
}

.range-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 20px;
  background: transparent;
  pointer-events: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.range-input::-webkit-slider-thumb {
  height: 20px;
  width: 20px;
  background: var(--violet);
  border-radius: 50%;
  border: none;
  cursor: pointer;
  pointer-events: all;
  -webkit-appearance: none;
}

.range-input::-moz-range-thumb {
  height: 20px;
  width: 20px;
  background: var(--violet);
  border-radius: 50%;
  border: none;
  cursor: pointer;
  pointer-events: all;
}

.range-track {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 4px;
  background: #e9ecef;
  border-radius: 2px;
  transform: translateY(-50%);
}

.range-progress {
  position: absolute;
  height: 100%;
  background: var(--violet);
  border-radius: 2px;
}
</style>