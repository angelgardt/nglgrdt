<template>
  <div class="lang-switcher">
    <button
      v-for="lang in availableLocales"
      :key="lang"
      :class="{ active: locale == lang }"
      @click="setLocale(lang)"
    >
      {{ getLangLabel(lang) }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale, availableLocales } = useI18n({ useScope: 'global' })

const setLocale = (lang: string) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
}

const getLangLabel = (lang: string) => {
  const labels: Record<string, string> = {
    ru: 'RU',
    en: 'EN',
  }
  return labels[lang] || lang.toUpperCase()
}
</script>
