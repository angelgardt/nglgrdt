<template>
    <h2>{{ header }}</h2>
    <div v-for="copyright in copyrights" :key="copyright">
      <ItemComp
      :title="copyright.title[lang]"
      :caption="copyright.description[lang]"
      :subtitle="copyright.author[lang]"
      :date="copyright.year"/>
    </div>
</template>

<script>
import CopyrightsJSON from '@/content/cv/Copyrights.json'
import ItemComp from './ItemComp.vue'

export default {
  name: 'CopyrightsSection',
  props: {
    header: String,
    lang: String
  },
  data () {
    return {
      copyrights: CopyrightsJSON.copyrights
    }
  },
  components: {
    ItemComp
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";
</style>
