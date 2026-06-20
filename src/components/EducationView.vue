<template>
  <section class="container">
    <h2>{{ commonData.sections.education.title }}</h2>

    <div class="education-list">
      <EducationCard
        v-for="edu in educationData.list"
        :key="edu.id"
        :edu="edu"
        :labs="commonData.labels.education"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import EducationCard from './EducationCard.vue'
import educationData from '@/locales/ru/about/education.json'
import commonData from '@/locales/ru/about/common.json'

const { t } = useI18n()
</script>
