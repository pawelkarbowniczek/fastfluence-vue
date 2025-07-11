<template>
  <div class="landing-page">
    <div class="container">
      <div class="text-center py-5">
        <h1 class="display-1 fw-bold mb-4">
          Znajdź idealną współpracę
        </h1>
        <p class="fs-5 text-muted mb-5">
          Łączymy marki z influencerami dla skutecznych kampanii marketingowych
        </p>

        <div class="hero-container">
          <HeroCircles @select-role="handleRoleSelection" />
        </div>

        <div class="auth-links mt-4">
          <router-link to="/login" class="btn btn-outline-primary me-3">
            Masz już konto? Zaloguj się
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import HeroCircles from '../components/HeroCircles.vue'
import type { UserRole } from '../types'

const router = useRouter()

const handleRoleSelection = (role: UserRole) => {
  router.push(`/register/${role}`)
}
</script>

<style scoped>
.landing-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
}

.hero-container {
  margin: 2rem 0;
}

.auth-links {
  margin: 2rem 0;
}
</style>