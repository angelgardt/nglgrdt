<template>
    <h2>{{ header }}</h2>
    <div v-for="(subsec, key, idx) in interests"
    :key = idx>
    <h3>{{ subheaders[key] }}</h3>
        <BubbleComp
        :bubbles="subsec[lang]"
        :align="'center'"
        />
    </div>
</template>

<script>
import BubbleComp from './BubbleComp.vue'
import InterestsJSON from '@/content/cv/Interests.json'

export default {
  name: 'InterestsSection',
  props: {
    lang: String,
    header: String,
    subheaders: String
  },
  data () {
    return {
      interests: InterestsJSON
    }
  },
  components: {
    BubbleComp
  }
}
</script>
