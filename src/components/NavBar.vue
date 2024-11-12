<template>
    <nav class="nav-secondary">
        <a v-for="item in NavAuthor" :key="item"
        href="">{{ item[lang].toLowerCase() }}</a>
    </nav>
</template>

<script>
import NavAuthorJSON from '@/content/NavAuthor.json'

export default {
  name: 'NavBar',
  inject: ['lang'],
  data () {
    return {
      NavAuthor: NavAuthorJSON
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";

nav.nav-secondary {
    a {
        display: inline-block;
        padding: 1em 1em;
        font-weight: 400;
        color: $tintedblack;
        &:hover {
            background-color: $shadedwhite;
        }
    }
}
</style>
