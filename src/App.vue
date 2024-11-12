<template>
  <HeaderComp/>
  <nav class="nav-main">
    <router-link to="/">home</router-link>
    <router-link to="/author">author</router-link>
  </nav>
  <router-view/>
  <FooterComp/>
</template>

<script>
import HeaderComp from './components/HeaderComp.vue'
import FooterComp from './components/FooterComp.vue'

export default {
  name: 'App',
  components: {
    HeaderComp,
    FooterComp
  }
}
</script>
<style lang="scss">
@import "@/assets/variables.scss";
@import "@/assets/fonts.scss";

body {
  margin: 0;
  padding-left: 0;
}

#app {
  font-family: Montserrat, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
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
