<template>
  <div class="lang-switcher-wrapper">
    <div class="lang-switcher">
      <select
      v-model="lang"
      @change="changeLang()">
          <option>en</option>
          <option>ru</option>
      </select>
    </div>
  </div>
  <HeaderComp/>
  <nav class="nav-main">
    <router-link to="/">{{ Nav.home[lang] }}</router-link>
    <router-link to="/author">{{ Nav.author[lang] }}</router-link>
  </nav>
  <router-view :lang="lang"/>
  <FooterComp/>
</template>

<script>
import HeaderComp from './components/HeaderComp.vue'
import FooterComp from './components/FooterComp.vue'
import NavJSON from './content/Nav.json'

export default {
  name: 'App',
  data () {
    return {
      lang: 'en',
      Nav: NavJSON
    }
  },
  provide () {
    return {
      getLang: () => this.lang
    }
  },
  methods: {
    changeLang () {
      console.log('changeLang')
    }
  },
  components: {
    HeaderComp,
    FooterComp
  }
}
</script>

<style lang="scss">
@import "@/assets/fonts.scss";
@import "@/assets/style.scss"
</style>
