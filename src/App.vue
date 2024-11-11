<template>
  <HeaderComp/>
  <nav>
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

nav {
  margin-bottom: 2em;
  text-align: center;
  background-color: $almostblack;

  a {
    display: inline-block;
    padding: .5em 0.5em 1em .5em;
    font-weight: 400;
    font-size: 1.1em;
    color: $almostwhite;
    text-decoration: none;
    &.router-link-exact-active {
      color: $tintedgray;
    }
    &:hover {
      background-color: $tintedblack;
    }
  }
}
</style>
