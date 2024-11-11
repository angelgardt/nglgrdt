<template>
  <NavBar/>
  <BasicSection/>
  <div class="content">
    <WorkExperienceSection/>
    <InterestsSection/>
    <EducationMainSection/>
    <EducationAdditionalSection/>
    <AchievementSection/>
    <LanguagesSection/>
    <SkillsSection/>
    <ResearchSection/>
    <CopyrightsSection/>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import EducationMainSection from '@/components/EducationMainSection.vue'
import CopyrightsSection from '@/components/CopyrightsSection.vue'
import BasicSection from '@/components/BasicSection.vue'

export default {
  name: 'AuthorView',
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
