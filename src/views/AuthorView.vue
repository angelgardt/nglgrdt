<template>
  <NavBar/>
  <BasicSection/>
  <WorkExperienceSection/>
  <InterestsSection/>
  <EducationMainSection/>
  <EducationAdditionalSection/>
  <AchievementSection/>
  <LanguagesSection/>
  <SkillsSection/>
  <ResearchSection/>
  <CopyrightsSection/>
</template>

<script>
import EducationMainSection from '@/components/EducationMainSection.vue'
import CopyrightsSection from '@/components/CopyrightsSection.vue'
import BasicSection from '@/components/BasicSection.vue'

export default {
  name: 'AuthorView',
  components: {
    BasicSection,
    EducationMainSection,
    CopyrightsSection
  }
}

</script>
