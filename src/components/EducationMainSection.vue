<template>
    <a name="education"></a>
    <h2>Education</h2>
    <div v-for="edu in edu" :key="edu">
      <div>{{ edu.years }}</div>
      <div>{{ edu.uni }}</div>
      <div>{{ edu.faculty }}</div>
      <div>{{ edu.program }}</div>
      <div>{{ edu.spec }}</div>
      <div>{{ edu.field }}</div>
      <div>{{ edu.gpa }}</div>
      <div v-if="edu.thesis">
        <div>Thesis Info</div>
        <div>{{ edu.thesis.title }}</div>
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
