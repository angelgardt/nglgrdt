<template>
  <details class="thesis-details">
    <summary>{{ t('labels.thesis') }}</summary>
    <div class="thesis-content">
      <p>
        <span class="thesis-content-name">{{ t('labels.title') }}</span
        >:
        <span class="thesis-content-person">{{ thesis.title }}</span>
      </p>
      <p>
        <span class="thesis-content-name">{{ t('labels.supervisor') }}</span
        >: <span class="thesis-content-person">{{ thesis.supervisor.name }}</span
        >,
        <span class="thesis-content-person-title">{{ thesis.supervisor.title }}</span>
      </p>
      <p>
        <span class="thesis-content-name">{{ t('labels.advisor') }}</span
        >: <span class="thesis-content-person">{{ thesis.advisor.name }}</span
        >,
        <span class="thesis-content-person-title">{{ thesis.advisor.title }}</span>
      </p>

      <div class="thesis-grades">
        <p>
          <span>{{ t('labels.grade_supervisor') }}</span
          >:
          <span>{{ thesis.grades.supervisor }}</span>
        </p>
        <p>
          <span>{{ t('labels.grade_reviewer') }}</span
          >:
          <span>{{ thesis.grades.reviewer }}</span>
        </p>
        <p>
          <span>{{ t('labels.grade_commission') }}</span
          >:
          <span>{{ thesis.grades.commission }}</span>
        </p>
      </div>
    </div>
  </details>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
interface ThesisData {
  title: string
  supervisor: string
  advisor: string
  reviewer: string
  grades: {
    supervisor: string
    reviewer: string
    commission: string
  }
}

const { t } = useI18n()

defineProps<{
  thesis: ThesisData
}>()
</script>
