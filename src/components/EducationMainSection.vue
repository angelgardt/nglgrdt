<template>
    <h2>{{ eduHeader }}</h2>
    <div
    class="edu"
    v-for="edu in edu"
    :key="edu">
      <div class="years">{{ edu.years }}</div>
      <div class="uni">{{ edu.uni[lang] }}</div>
      <div class="faculty">{{ edu.faculty[lang] }}</div>
      <div v-if="edu.program" class="program">{{ edu.program[lang] }}</div>
      <div v-if="edu.spec" class="spec">{{ edu.spec[lang] }}</div>
      <div class="field">{{ edu.field[lang] }}</div>
      <div v-if="edu.gpa" class="gpa">{{ edu.gpa }}</div>
      <EduThesisInfo :edu="edu"/>
    </div>
</template>

<script>
import EducationMainJSON from '@/content/EducationMainSection.json'
import EduThesisInfo from './EduThesisInfo.vue'

export default {
  name: 'EducationMainSection',
  inject: ['lang'],
  props: {
    eduHeader: String
  },
  data () {
    return {
      edu: EducationMainJSON
    }
  },
  components: {
    EduThesisInfo
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";
@import "@/assets/style.scss";

.edu {
  margin: 1em;
  padding: 1em;
  border-radius: 10px;
  background-color: $almostwhite;
  .years, .uni, .faculty, .program, .field, .gpa, .spec {
    line-height: 1.5em;
  }
  .uni {
    font-weight: 700;
  }
  .gpa {
    font-weight: 600;
  }
}
</style>
