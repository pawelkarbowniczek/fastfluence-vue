<template>
  <button 
    :class="['btn', ...classes]"
    @click="$emit('click', $event)"
    :disabled="disabled"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
interface Props {
  classes?: string[]
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  classes: () => [],
  disabled: false
})

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>