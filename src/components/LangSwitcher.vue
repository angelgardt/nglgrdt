<template>
  <div class="lang-switcher">
    <button
      v-for="lang in availableLocales"
      :key="lang"
      :class="{ active: locale == lang }"
      @click="setLocale(lang)"
    ></button>
  </div>
</template>

<script lang="ts">
import { useI18n } from 'vue-i18n'

const { locale, availableLocales } = useI18n()

const setLocale = (lang: string) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>
