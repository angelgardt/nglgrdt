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
import CopyRightsJSON from '@/content/CopyRights.json'

export default {
  name: 'CopyRights',
  data () {
    return {
      copyrights: CopyRightsJSON
    }
  }
}
</script>
