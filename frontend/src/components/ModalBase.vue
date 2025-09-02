<template>
  <div class="modal d-block" tabindex="-1" @click.self="$emit('close')">
    <div class="modal-dialog">
      <div class="modal-content">
        <button
          type="button"
          class="btn-close position-absolute top-0 end-0 m-3"
          @click="$emit('close')"
          style="z-index: 1060;"
          aria-label="Close"
        ></button>
        <slot />
      </div>
    </div>
  </div>
  <div class="modal-backdrop show"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits<{
  close: []
}>()

const handleEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  // Prevent body scrolling when modal is open
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  // Restore body scrolling
  document.body.style.overflow = ''
})
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.btn-close {
  z-index: 1060;
}
</style>