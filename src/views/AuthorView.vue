<template>
  <NavBar :lang="lang"/>
  <BasicSection :lang="lang"/>
  <div class="content">
    <WorkExperience
    :header="NavCV.workExperience.header[lang]"
    :subheaders="NavCV.workExperience.subheaders[lang]"
    :lang="lang"
    />
    <InterestsSection
    :header="NavCV.interests.header[lang]"
    :subheaders="NavCV.interests.subheaders[lang]"
    :lang="lang"
    />
    <EducationMainSection
    :header="NavCV.eduMain.header[lang]"
    :lang="lang"
    />
    <SkillsSection
    :header="NavCV.skills.header[lang]"
    :subheaders="NavCV.skills.subheaders[lang]"
    :lang="lang"/>
    <CopyrightsSection
    :header="NavCV.copyrights.header[lang]"
    :lang="lang"
    />
  </div>
</template>

<script>
import NavBar from '@/components/NavBarCV.vue'
import NavCVJSON from '@/content/cv/NavCV.json'
import BasicSection from '@/components/BasicSection.vue'
import WorkExperience from '@/components/WorkExperience.vue'
import InterestsSection from '@/components/InterestsSection.vue'
import EducationMainSection from '@/components/EducationMainSection.vue'
import SkillsSection from '@/components/SkillsSection.vue'
import CopyrightsSection from '@/components/CopyrightsSection.vue'

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
    InterestsSection,
    EducationMainSection,
    SkillsSection,
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
