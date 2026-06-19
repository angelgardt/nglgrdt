<template>
  <section class="container">
    <h2>{{ t('sections.education') }}</h2>

    <EducationCard edu-key=""
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import EducationCard from './EducationCard.vue';

const { t } = useI18n()
</script>
