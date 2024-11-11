<template>
    <h2>Copyrights</h2>
    <div v-for="copyright in copyrights" :key="copyright">
        <div>{{ copyright.title }}</div>
        <div>{{ copyright.description }}</div>
        <div>{{ copyright.author }}</div>
        <div>{{ copyright.year }}</div>
    </div>
</template>

<script>
import CopyrightsJSON from '@/content/CopyrightsSection.json'

export default {
  name: 'CopyrightsSection',
  data () {
    return {
      copyrights: CopyrightsJSON
    }
  }
}
</script>
