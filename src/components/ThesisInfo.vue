<template>
    <div class="thesis">
        <div class="thesis-header"
        @click="showThesis()">
            {{ thesis.header[lang] }}
        </div>
        <div class="thesis-info">
            <div v-if="thesisShown">
                <div class="title">
                    <span class="name">{{ thesis.name[lang] }}: </span>
                    <span class="title">{{ thesis.title[lang] }}</span>
                </div>
                <div class="supervisor">
                    <span class="title">{{ thesis.supervisor.title[lang] }}: </span>
                    <span class="name">{{ thesis.supervisor.name[lang] }}, </span>
                    <span class="degree">{{ thesis.supervisor.degree[lang] }}</span>
                </div>
                <div class="advisor">
                    <span class="title">{{ thesis.advisor.title[lang] }}: </span>
                    <span class="name">{{ thesis.advisor.name[lang] }}, </span>
                    <span class="degree">{{ thesis.advisor.degree[lang] }}</span>
                </div>
                <div class="reviewer">
                    <span class="title">{{ thesis.reviewer.title[lang] }}: </span>
                    <span class="name">{{ thesis.reviewer.name[lang] }}, </span>
                    <span class="degree">{{ thesis.advisor.degree[lang] }}</span>
                </div>
                <div class="grades"
                v-for="(grade, idx) in thesis.grades"
                :key="idx">
                    {{ grade[lang] }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'ThesisInfo',
  props: {
    thesis: Object,
    lang: String
  },
  data () {
    return {
      thesisShown: true
    }
  },
  methods: {
    showThesis () {
      this.thesisShown = !this.thesisShown
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";
</style>
