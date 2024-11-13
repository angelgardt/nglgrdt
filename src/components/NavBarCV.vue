<template>
    <nav class="nav-secondary">
        <a v-for="(item, idx) in NavCV" :key="idx"
        href="">{{ item.header[lang] }}</a>
    </nav>
</template>

<script>
import NavCVJSON from '@/content/cv/NavCV.json'

export default {
  name: 'NavBarCV',
  props: {
    lang: String
  },
  data () {
    return {
      NavCV: NavCVJSON
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";

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
