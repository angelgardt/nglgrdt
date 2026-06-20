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

<style lang="scss">
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  nav {
    display: flex;
    align-items: center;
    .logo {
      background-color: red;
      flex-shrink: 0;
    }
    ul.nav-links {
      display: flex;
      justify-content: center;
      flex: 1;
      max-width: 1280px;
      margin: 0 auto;
      list-style-type: none;
      li {
        display: inline;
        background-color: yellow;
        vertical-align: middle;
        a {
          padding: 1em;
          text-decoration: none;
        }
      }
    }
    .lang-switcher {
      margin-left: auto;
      flex-shrink: 0;
      button {
        background-color: green;
        color: white;
        border: 1px solid white;
      }
    }
  }
}

main {
  flex-grow: 1;
  margin: 0 auto;
  max-width: 1280px;
  width: 100%;
}

footer {
  background-color: #f5f5f5;
  padding: 1rem;
  text-align: center;
}
</style>
