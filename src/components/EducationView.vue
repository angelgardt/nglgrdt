<template>
  <section class="container">
    <h2>{{ t('sections.education') }}</h2>

    <div class="education-list">
      <EducationCard v-for="edu in educationData.list" :key="edu.id" :edu="edu" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import EducationCard from './EducationCard.vue'
import educationData from '@/locales/ru/about/education.json'

const { t } = useI18n()
</script>
