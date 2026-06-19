<template>
  <article class="education-card">
    <p class="years">{{ edu.start }}–{{ edu.end }}, {{ edu.level }}</p>
    <p class="university">{{ edu.university }}</p>
    <p v-if="edu.faculty" class="faculty">{{ edu.faculty }}</p>
    <p v-if="edu.program" class="program">{{ edu.program }}</p>
    <p v-if="edu.track" class="track">{{ edu.track }}</p>
    <p v-if="edu.gpa" class="gpa">{{ edu.gpa }}</p>
  </article>
</template>

<script setup lang="ts">
interface Education {
  id: string
  type: string
  level: string
  university: string
  faculty?: string
  program?: string
  track?: string
  start: string
  end: string
  thesis?: {
    title: string
    supervisor: string
    advisor?: string
    reviewer?: string
    grades?: {
      supervisor: string
      reviewer: string
      commission: string
    }
  }
  grade?: {
    supervisor: string
    reviewer: string
    commission: string
  }
}

defineProps<{
  edu: Education
}>()
</script>
