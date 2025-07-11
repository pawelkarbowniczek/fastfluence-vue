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

        <div v-if="!showRegistration" class="hero-container">
          <HeroCircles @select-role="handleRoleSelection" />
        </div>

        <div v-else class="registration-container">
          <AuthRegister
            :role="selectedRole"
            @success="handleRegistrationSuccess"
            @show-login="showLogin = true"
          />
        </div>
      </div>
    </div>

    <!-- Login Modal -->
    <AuthLogin
      v-if="showLogin"
      @close="showLogin = false"
      @success="handleLoginSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import HeroCircles from '../components/HeroCircles.vue'
import AuthRegister from '../components/AuthRegister.vue'
import AuthLogin from '../components/AuthLogin.vue'
import type { UserRole } from '../types'

const router = useRouter()

const showRegistration = ref(false)
const showLogin = ref(false)
const selectedRole = ref<UserRole>('advertiser')

const handleRoleSelection = (role: UserRole) => {
  selectedRole.value = role
  showRegistration.value = true
}

const handleRegistrationSuccess = () => {
  router.push('/dashboard')
}

const handleLoginSuccess = () => {
  showLogin.value = false
  router.push('/dashboard')
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

.registration-container {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}
</style>