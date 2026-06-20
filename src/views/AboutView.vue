<template>
  <section class="section container">
    <h1>Extended CV</h1>
    <EducationView />
  </section>
</template>

<script setup lang="ts">
import EducationView from '@/components/EducationView.vue'
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
