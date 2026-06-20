<template>
  <section class="container">
    <h2>{{ educationTitle }}</h2>

    <div class="education-list">
      <EducationCard v-for="edu in educationList" :key="edu.id" :edu="edu" :labs="educationLabs" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import EducationCard from './EducationCard.vue'

const { tm } = useI18n()

const educationList = computed(() => tm('education.list'))
const educationLabs = computed(() => tm('about.labels.education'))
const educationTitle = computed(() => tm('about.sections.education.title'))
</script>
