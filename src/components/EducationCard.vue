<template>
  <article class="education-card">
    <p class="years">{{ edu.start }}–{{ edu.end }}, {{ edu.level }}</p>
    <p class="university">{{ edu.university }}</p>
    <p>
      <span v-if="edu.institute" class="faculty">{{ edu.institute }}</span>
      <span v-if="edu.institute && edu.faculty">, </span>
      <span v-if="edu.faculty" class="faculty">{{ edu.faculty }}</span>
      <span v-if="edu.faculty && edu.department">, </span>
      <span v-if="edu.department" class="department">{{ edu.department }}</span>
    </p>
    <p v-if="edu.program" class="program">
      <span>{{ labs.program }}&nbsp;</span>
      <span>{{ edu.program }}</span>
    </p>
    <p v-if="edu.track" class="track">
      <span>{{ labs.track }}&nbsp;</span>
      <span>{{ edu.track }}</span>
    </p>
    <p class="spec">
      <span>{{ labs.spec }}&nbsp;</span>
      <span>{{ edu.spec }}</span>
      <span v-if="edu.qualification" class="qualification">
        <span>, {{ labs.qualification }}&nbsp;</span>
        <span>{{ edu.qualification }}</span>
      </span>
    </p>
    <div v-if="edu.minor" class="minor">
      <p>{{ labs.minor }}</p>
      <p v-if="edu.minor.institute">{{ edu.minor.institute }}</p>
      <p v-if="edu.minor.faculty">{{ edu.minor.faculty }}</p>
      <p v-if="edu.program" class="program">
        <span>{{ labs.program }}&nbsp;</span>
        <span>{{ edu.minor.program }}</span>
      </p>
      <p class="spec">
        <span>{{ labs.spec }}&nbsp;</span>
        <span>{{ edu.minor.spec }}</span>
      </p>
    </div>
    <p v-if="edu.gpa" class="gpa">
      <span>{{ labs.gpa }}: </span>
      <span>{{ edu.gpa }}</span>
    </p>
    <details v-if="edu.thesis" class="thesis" open>
      <summary v-if="edu.lvl == 'master'">{{ labs.thesis.master }}</summary>
      <summary v-if="edu.lvl == 'bachelor'">{{ labs.thesis.bachelor }}</summary>
      <p class="thesis-title">
        <span>{{ labs.thesis.title }}: </span>
        <span>{{ edu.thesis.title }}</span>
      </p>
      <p class="thesis-supervisor">
        <span>{{ labs.thesis.supervisor }}: </span>
        <span>{{ edu.thesis.supervisor.name }}</span>
        <span>, {{ edu.thesis.supervisor.title }}</span>
      </p>
      <p class="thesis-advisor">
        <span>{{ labs.thesis.advisor }}: </span>
        <span>{{ edu.thesis.advisor?.name }}</span>
        <span>, {{ edu.thesis.advisor?.title }}</span>
      </p>
      <p class="thesis-reviewer">
        <span>{{ labs.thesis.reviewer }}: </span>
        <span>{{ edu.thesis.reviewer?.name }}</span>
        <span>, {{ edu.thesis.reviewer?.title }}</span>
      </p>
      <div class="thesis-grades">
        <p class="thesis-grade-supervisor">
          <span>{{ labs.thesis.grades.supervisor }}: </span>
          <span>{{ edu.thesis.grades?.supervisor }}</span>
        </p>
        <p class="thesis-grade-reviewer">
          <span>{{ labs.thesis.grades.reviewer }}: </span>
          <span>{{ edu.thesis.grades?.reviewer }}</span>
        </p>
        <p class="thesis-grade-commission">
          <span>{{ labs.thesis.grades.commission }}: </span>
          <span>{{ edu.thesis.grades?.commission }}</span>
        </p>
      </div>
    </details>
  </article>
</template>

<style lang="scss">
.education-card {
  border: 1px solid black;
}
</style>

<script setup lang="ts">
interface Education {
  id: string
  lvl: string
  level: string
  start: string
  end: string
  university: string
  institute?: string
  faculty?: string
  department?: string
  program?: string
  track?: string
  spec: string
  qualification: string
  gpa: string
  minor?: {
    faculty?: string
    institute?: string
    program?: string
    spec?: string
  }
  thesis?: {
    title: string
    supervisor: {
      name: string
      title: string
    }
    advisor?: {
      name: string
      title: string
    }
    reviewer?: {
      name: string
      title: string
    }
    grades?: {
      supervisor: string
      reviewer: string
      commission: string
    }
  }
}

interface Labs {
  program: string
  level: string
  track: string
  spec: string
  qualification: string
  gpa: string
  minor: string
  thesis: {
    bachelor: string
    master: string
    title: string
    supervisor: string
    advisor: string
    reviewer: string
    grades: {
      supervisor: string
      reviewer: string
      commission: string
    }
  }
}

defineProps<{
  edu: Education
  labs: Labs
}>()
</script>
