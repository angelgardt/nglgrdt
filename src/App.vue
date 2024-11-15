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
@import "@/assets/style.scss";

body {
  margin: 0;
  padding-left: 0;
}
.lang-switcher-wrapper {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  z-index: 99;
  .lang-switcher {
      position: sticky;
      top: 0;
      padding: 1em;
      select {
        font-size: 1em;
        padding: .1em;
        background-color: $almostblack;
        color: $almostwhite;
        border-color: $almostwhite;
        border-radius: 5px;
      }
  }
}

#app {
  font-family: Montserrat, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #000000;
}

h1 {
  text-align: left;
  margin-bottom: 0;
}

nav {
  text-align: center;
  a {
    text-decoration: none;
  }
  &.nav-main {
    position: sticky;
    top: 0;
    background-color: $almostblack;
    a {
      display: inline-block;
      padding: .5em 1em 1em 1em;
      font-weight: 400;
      font-size: 1.1em;
      color: $almostwhite;
      &.router-link-exact-active {
        color: $tintedgray;
      }
      &:hover {
        background-color: $tintedblack;
      }
    }
  }
}
</style>
