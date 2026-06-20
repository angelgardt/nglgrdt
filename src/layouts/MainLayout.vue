<template>
  <div class="layout">
    <header>
      <nav class="container nav">
        <RouterLink to="/" class="logo">A. N. Angelgardt</RouterLink>
        <ul class="nav-links">
          <li><RouterLink to="/about">Обо мне</RouterLink></li>
          <li><RouterLink to="/projects">Проекты</RouterLink></li>
          <li><RouterLink to="/publications">Публикации</RouterLink></li>
        </ul>
        <!--<LangSwitcher />-->
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

const currentYear = computed(() => new Date().getFullYear())
</script>

<style lang="scss"></style>
