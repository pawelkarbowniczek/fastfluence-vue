<template>
  <div class="not-found-page">
    <div class="container">
      <div class="text-center">
        <div class="error-code">404</div>
        <h1 class="mb-4">Strona nie została znaleziona</h1>
        <p class="fs-5 text-muted mb-4">
          Przepraszamy, ale strona której szukasz nie istnieje.
        </p>
        <router-link to="/" class="btn btn-primary btn-lg">
          Powrót do strony głównej
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No script needed for this simple component
</script>

<style scoped>
.not-found-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: var(--violet);
  line-height: 1;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .error-code {
    font-size: 4rem;
  }
}
</style>