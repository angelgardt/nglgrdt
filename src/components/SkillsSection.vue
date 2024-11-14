<template>
    <h2>{{ header }}</h2>
    <div v-for="(subsec, key, idx) in skills"
    :key="idx">
        <div v-if="subheaders[key].name">
            <h3>{{ subheaders[key].name }}</h3>
            <div class="bubble-column-wrapper">
              <div
              v-for="(subsubsec, subkey, idx) in subsec"
              :key="idx">
                <div class="bubble-column">
                  <h4>{{ subheaders[key].subheaders[subkey] }}</h4>
                  <BubbleComp
                  :bubbles="subsubsec[lang]"
                  />
                </div>
              </div>
            </div>
        </div>
        <h3 v-else>{{ subheaders[key] }}</h3>
        <BubbleComp
        :bubbles="subsec[lang]"
        />
    </div>
</template>

<script>
import SkillsJSON from '@/content/cv/Skills.json'
import BubbleComp from './BubbleComp.vue'

export default {
  name: 'SkillsSection',
  props: {
    header: String,
    subheaders: String,
    lang: String
  },
  data () {
    return {
      skills: SkillsJSON
    }
  },
  components: {
    BubbleComp
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";

.bubble-column-wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1em;
}
</style>
