<template>
  <div class="layout">
    <header>
      <nav class="container nav">
        <RouterLink to="/" class="logo">A. N. Angelgardt</RouterLink>
        <ul class="nav-links">
          <li>
            <RouterLink to="/about">{{ navLabels.about }}</RouterLink>
          </li>
          <li>
            <RouterLink to="/projects">{{ navLabels.projects }}</RouterLink>
          </li>
          <li>
            <RouterLink to="/publications">{{ navLabels.publications }}</RouterLink>
          </li>
        </ul>
        <LangSwitcher />
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>

    <footer class="footer">
      <div class="container">
        <p>© 2020–{{ currentYear }} А. Н. Ангельгардт</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import LangSwitcher from '@/components/LangSwitcher.vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const currentYear = computed(() => new Date().getFullYear())

const { tm } = useI18n()
const navLabels = computed(() => tm('nav'))
</script>

<style lang="scss"></style>
