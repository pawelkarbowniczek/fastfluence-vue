<template>
  <div class="card h-100 creator-card">
    <div class="card-body">
      <div class="d-flex align-items-center mb-3">
        <div class="avatar-placeholder me-3">
          {{ creator.display_name.charAt(0).toUpperCase() }}
        </div>
        <div>
          <h5 class="card-title mb-1">{{ creator.display_name }}</h5>
          <p class="text-muted small mb-0">{{ creator.contact_email }}</p>
        </div>
      </div>
      
      <div class="creator-info">
        <div v-if="creator.website_url" class="mb-2">
          <small class="text-muted">Strona:</small>
          <a :href="creator.website_url" target="_blank" class="text-decoration-none d-block">
            {{ creator.website_url }}
          </a>
        </div>
        
        <div v-if="creator.social_links.length" class="mb-3">
          <small class="text-muted">Media społecznościowe:</small>
          <div class="social-links">
            <a 
              v-for="link in creator.social_links" 
              :key="link"
              :href="link" 
              target="_blank"
              class="badge bg-secondary text-decoration-none me-1"
            >
              {{ getSocialPlatform(link) }}
            </a>
          </div>
        </div>
        
        <div v-if="creator.portfolio.length" class="portfolio-section">
          <small class="text-muted">Portfolio:</small>
          <div class="portfolio-items">
            <div 
              v-for="item in creator.portfolio.slice(0, 2)" 
              :key="item.title"
              class="portfolio-item mb-2"
            >
              <div class="fw-semibold">{{ item.title }}</div>
              <div class="text-muted small">{{ item.brand_name }} - {{ item.role_in_campaign }}</div>
              <div class="text-muted small">{{ item.short_description }}</div>
            </div>
            <div v-if="creator.portfolio.length > 2" class="text-muted small">
              +{{ creator.portfolio.length - 2 }} więcej projektów
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card-footer bg-transparent">
      <div class="d-flex gap-2">
        <button class="btn btn-outline-primary btn-sm flex-fill">
          Zobacz profil
        </button>
        <button v-if="canContact" class="btn btn-primary btn-sm flex-fill">
          Skontaktuj się
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import type { User } from '../types'

interface Props {
  creator: User
}

const props = defineProps<Props>()

const authStore = useAuthStore()

const canContact = computed(() => {
  return authStore.isAdvertiser && authStore.user?.id !== props.creator.id
})

const getSocialPlatform = (url: string) => {
  if (url.includes('instagram.com')) return 'Instagram'
  if (url.includes('tiktok.com')) return 'TikTok'
  if (url.includes('youtube.com')) return 'YouTube'
  if (url.includes('facebook.com')) return 'Facebook'
  if (url.includes('linkedin.com')) return 'LinkedIn'
  return 'Link'
}
</script>

<style scoped>
.creator-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.creator-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.avatar-placeholder {
  width: 50px;
  height: 50px;
  background: var(--violet);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
}

.portfolio-item {
  border-left: 3px solid var(--violet);
  padding-left: 0.5rem;
}

.social-links {
  margin-top: 0.25rem;
}
</style>