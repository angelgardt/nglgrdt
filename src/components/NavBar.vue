<template>
    <nav class="nav-secondary">
        <a v-for="(item, idx) in NavAuthor" :key="idx"
        href="">{{ item[lang] }}</a>
    </nav>
</template>

<script>
import NavAuthorJSON from '@/content/NavAuthor.json'

export default {
  name: 'NavBar',
  props: {
    lang: String
  },
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
        text-transform: lowercase;
        &:hover {
            background-color: $shadedwhite;
        }
    }
}
</style>
