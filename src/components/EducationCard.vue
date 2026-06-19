<template>
  <article class="education-card">
    <p class="years">
      <span>{{ edu.start }}</span
      >–<span>{{ edu.end }}</span
      >, <span>{{ edu.level }}</span>
    </p>
    <p class="university">{{ edu.university }}</p>
    <p class="faculty"></p>
    <p class="program"></p>
  </article>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
</script>
