<template>
  <NavBar/>
  <BasicSection/>
  <div class="content">
    <EducationMainSection
    :edu-header="NavAuthor.eduMain[lang]"/>
    <CopyrightsSection/>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import NavAuthorJSON from '@/content/NavAuthor.json'
import EducationMainSection from '@/components/EducationMainSection.vue'
import CopyrightsSection from '@/components/CopyrightsSection.vue'
import BasicSection from '@/components/BasicSection.vue'

export default {
  name: 'AuthorView',
  inject: ['lang'],
  data () {
    return {
      NavAuthor: NavAuthorJSON
    }
  },
  components: {
    NavBar,
    BasicSection,
    EducationMainSection,
    CopyrightsSection
  }
}

</script>

<style scoped lang="scss">
.content {
  width: 1400px;
  margin: auto;
}
</style>
