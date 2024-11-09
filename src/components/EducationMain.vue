<template>
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
          <span>{{ edu.thesis.supervisor.name }}, </span>
          <span>{{ edu.thesis.supervisor.title }}</span>
        </div>
        <div>
          <span>{{ edu.thesis.advisor.name }}, </span>
          <span>{{ edu.thesis.advisor.title }}</span>
        </div>
        <div>
          <span>{{ edu.thesis.reviewer.name }}, </span>
          <span>{{ edu.thesis.reviewer.title }}</span>
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
export default {
  name: 'EducationMain',
  data () {
    return {
      edu: {
        edu2: {
          uni: 'HSE University',
          years: '2021–2023',
          faculty: 'Faculty of Humanities',
          program: '“Russian as a Foreign Language in Cross-Linguistic and Cross-Cultural Perspective” program (Master\'s Degree)',
          spec: null,
          field: 'Field of Study 45.04.03 "Fundamental and Applied Linguistics"',
          gpa: 'GPA: 8.44 / 10',
          thesis: {
            title: 'Title: “Development of Speech Recognition Based Application for RFL Students”',
            supervisor: {
              name: 'Inna Sieber',
              title: 'Candidate of Sciences (PhD), Associate Professor, School of Linguistics, HSE University'
            },
            advisor: {
              name: 'George Moroz',
              title: 'Candidate of Sciences (PhD), Associate Professor, School of Linguistics, HSE University'
            },
            reviewer: {
              name: 'Olga Buivolova',
              title: 'Candidate of Sciences (PhD), Research Fellow, Center for Language and Brain, HSE University'
            },
            grades: {
              supervisor: 'Supervisor\'s Grade: 10 / A+ / “Excellent”',
              reviewer: 'Reviewer\'s Grade: 10 / A+ / “Excellent”',
              board: 'State Certification Board Grade: 10 / A+ / “Excellent”'
            }
          }
        },
        edu1: {
          uni: 'HSE University',
          years: '2017–2021',
          faculty: 'Faculty of Social Sciences',
          program: '"Psychology" program (Bachelor\'s Degree)',
          spec: '“Cognitive Psychology & Psychophysiology” and “Organizational Psychology” tracks',
          field: 'Field of Study 37.03.01 “Psychology”',
          gpa: 'GPA: 8.44 / 10',
          thesis: {
            title: 'Title: “Assessment of Trust in Artificial Intelligent Agents: Tool Development”',
            supervisor: {
              name: 'Elena Gorbunova',
              title: 'Candidate of Sciences (PhD), Associate Professor, School of Psychology, HSE University'
            },
            advisor: {
              name: 'Maria Chumakova',
              title: 'Candidate of Sciences (PhD), Associate Professor, School of Psychology, HSE University'
            },
            reviewer: {
              name: 'Alexander Poddiakov',
              title: 'Doctor of Sciences, Tenured Professor, School of Psychology, HSE University'
            },
            grades: {
              supervisor: 'Supervisor\'s Grade: 10 / A+ / “Excellent”',
              reviewer: 'Reviewer\'s Grade: 10 / A+ / “Excellent”',
              board: 'State Certification Board Grade: 10 / A+ / “Excellent”'
            }
          }
        },
        edu0: {
          uni: 'Pavlov First Saint Petersburg State Medical University',
          years: '2014–2017',
          faculty: 'Faculty of Medicine (Specialist\'s Degree)',
          program: null,
          spec: 'Sports Medicine Department',
          field: 'Field of Study 31.05.01 “General Medicine”',
          gpa: null,
          thesis: null
        }
      }
    }
  }
}
</script>
