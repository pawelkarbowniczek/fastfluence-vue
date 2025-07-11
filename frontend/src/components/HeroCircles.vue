<template>
  <div class="hero-section d-flex justify-content-center align-items-center position-relative">
    <div class="hero-circle hero-circle-violet me-n5">
      <BtnCta 
        @click="$emit('selectRole', 'advertiser')"
        class="btn btn-primary btn-lg w-100 fw-bold"
      >
        Jestem reklamodawcą
      </BtnCta>
    </div>
    
    <div class="hero-circle hero-circle-lime ms-n5">
      <BtnCta 
        @click="$emit('selectRole', 'creator')"
        class="btn btn-success btn-lg w-100 fw-bold"
      >
        Jestem influencerem
      </BtnCta>
    </div>
    
    <div class="hero-logo">
      B
    </div>
  </div>
</template>

<script setup lang="ts">
import BtnCta from './BtnCta.vue'

defineEmits<{
  selectRole: [role: 'advertiser' | 'creator']
}>()
</script>

<style scoped>
.hero-section {
  min-height: 400px;
  padding: 2rem 0;
}

.hero-circle {
  z-index: 1;
}

.hero-logo {
  z-index: 10;
}
</style>