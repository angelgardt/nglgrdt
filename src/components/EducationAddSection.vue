<template>
    <h2>{{ header }}</h2>
    <div
    v-for="(subsec, key, idx) in eduAdd"
    :key="idx">
        <h3 v-if="subsec">{{ subheaders[key] }}</h3>
        <div v-if="key === 'moocs'">
          <div
          v-for="(item, idx) in subsec"
          :key="idx">
          <ItemComp
              :title="item[lang].title"
              :author="item[lang].author"
              :platform="item[lang].platform"
              :date="item[lang].date"
              />
          </div>
        </div>
        <div v-else>
          <div
          v-for="(item, idx) in subsec"
          :key="idx">
              <ItemComp
              :title="item[lang].title"
              :caption="item[lang].caption"
              :subtitle="item[lang].org"
              :date="item[lang].date"
              />
          </div>
        </div>
    </div>
</template>

<script>
import EducationAddJSON from '@/content/cv/EducationAdd.json'
import ItemComp from './ItemComp.vue'

export default {
  name: 'EducationAddSection',
  props: {
    lang: String,
    header: String,
    subheaders: Object
  },
  data () {
    return {
      eduAdd: EducationAddJSON
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
