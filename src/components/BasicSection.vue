<template>
    <h1>{{ basic.name }}</h1>
    <div>
      <span>{{ basic.city }}</span>, <span>{{ calcAge() }}</span> y. o.
    </div>
</template>

<script>
import BasicSectionJSON from '@/content/BasicSection.json'

export default {
  name: 'BasicSection',
  data () {
    return {
      basic: BasicSectionJSON
    }
  },
  methods: {
    calcAge () {
      return new Date(new Date() - new Date(this.basic.birth)).getUTCFullYear() - 1970
    }
  }
}
</script>
