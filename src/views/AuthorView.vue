<template>
  <NavBar :lang="lang"/>
  <BasicSection :lang="lang"/>
  <div class="content">
    <WorkExperience
    :header="NavCV.workExperience.header[lang]"
    :subheaders="NavCV.workExperience.subheaders[lang]"
    :lang="lang"/>
    <InterestsSection
    :header="NavCV.interests.header[lang]"
    />
    <EducationMainSection
    :header="NavCV.eduMain.header[lang]"
    :lang="lang"/>
    <CopyrightsSection
    :header="NavCV.copyrights.header[lang]"
    :lang="lang"/>
  </div>
</template>

<script>
import NavBar from '@/components/NavBarCV.vue'
import BasicSection from '@/components/BasicSection.vue'
import EducationMainSection from '@/components/EducationMainSection.vue'
import WorkExperience from '@/components/WorkExperience.vue'
import CopyrightsSection from '@/components/CopyrightsSection.vue'
import NavCVJSON from '@/content/cv/NavCV.json'

export default {
  name: 'AuthorView',
  props: {
    lang: String
  },
  data () {
    return {
      NavCV: NavCVJSON
    }
  },
  components: {
    NavBar,
    BasicSection,
    WorkExperience,
    EducationMainSection,
    CopyrightsSection
  }
}

</script>

<style lang="scss">
@import "@/assets/style.scss";

.content {
  width: 1400px;
  margin: auto;
}
</style>
