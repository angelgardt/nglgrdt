<template>
    <h2>{{ eduHeader }}</h2>
    <div
    class="edu"
    v-for="(edu, idx) in edu"
    :key="idx">
      <div class="years">{{ edu.years }}</div>
      <div class="uni">{{ edu.uni[lang] }}</div>
      <div class="faculty">{{ edu.faculty[lang] }}</div>
      <div v-if="edu.program" class="program">{{ edu.program[lang] }}</div>
      <div v-if="edu.spec" class="spec">{{ edu.spec[lang] }}</div>
      <div class="field">{{ edu.field[lang] }}</div>
      <div v-if="edu.gpa" class="gpa">{{ edu.gpa }}</div>
      <EduThesisInfo :edu="edu" :lang="lang"/>
      <div class="minor" v-if="edu.additional">
        <div class="name">{{ edu.additional.name[lang] }}</div>
        <div class="faculty">{{ edu.additional.faculty[lang] }}</div>
        <div class="program">{{ edu.additional.program[lang] }}</div>
        <div class="field">{{ edu.additional.field[lang] }}</div>
      </div>
    </div>
</template>

<script>
import EduThesisInfo from './EduThesisInfo.vue'
import EducationMainJSON from '@/content/cv/EducationMainSection.json'

export default {
  name: 'EducationMainSection',
  inject: ['lang'],
  props: {
    lang: String,
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
  margin: 1em 1em;
  padding: 1.5em 2em;
  border-radius: 10px;
  background-color: $almostwhite;
  .years, .uni, .faculty, .program, .spec {
    line-height: 1.5em;
  }
  .uni {
    font-weight: 700;
  }
  .faculty {
    font-weight: 500;
  }
  .field {
    font-size: .9em;
    line-height: 2em
  }
  .gpa {
    font-weight: 600;
    line-height: 2em;
  }
  .minor {
    margin-top: 2em;
    >.name {
      font-weight: 600;
    }
  }
}
</style>
