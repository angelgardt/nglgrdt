<template>
    <a name="education"></a>
    <h2>Education</h2>
    <div
    class="edu"
    v-for="edu in edu"
    :key="edu">
      <div class="years">{{ edu.years }}</div>
      <div class="uni">{{ edu.uni }}</div>
      <div class="faculty">{{ edu.faculty }}</div>
      <div class="program">{{ edu.program }}</div>
      <div class="spec">{{ edu.spec }}</div>
      <div class="field">{{ edu.field }}</div>
      <div class="gpa">{{ edu.gpa }}</div>
      <div
      class="thesis"
      v-if="edu.thesis">
        <div class="thesis-info">{{ edu.thesis.name }}</div>
        <div class="thesis-title">{{ edu.thesis.title }}</div>
        <div>
          <span>{{ edu.thesis.supervisor.title }}: </span>
          <span>{{ edu.thesis.supervisor.name }}, </span>
          <span>{{ edu.thesis.advisor.degree }}</span>
        </div>
        <div>
          <span>{{ edu.thesis.advisor.title }}: </span>
          <span>{{ edu.thesis.advisor.name }}, </span>
          <span>{{ edu.thesis.advisor.degree }}</span>
        </div>
        <div>
          <span>{{ edu.thesis.reviewer.title }}: </span>
          <span>{{ edu.thesis.reviewer.name }}, </span>
          <span>{{ edu.thesis.advisor.degree }}</span>
        </div>
        <div>
          <div>{{ edu.thesis.grades.supervisor }}</div>
          <div>{{ edu.thesis.grades.advisor }}</div>
          <div>{{ edu.thesis.grades.board }}</div>
        </div>
      </div>
    </div>
</template>

<script>
import EducationMainJSON from '@/content/EducationMainSection.json'

export default {
  name: 'EducationMainSection',
  data () {
    return {
      edu: EducationMainJSON
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";
@import "@/assets/style.scss";

.edu {
  background-color: $almostwhite;
}
</style>
