<template>
    <div
      class="thesis"
      v-if="edu.thesis">
        <div
        @click="showThesisInfo()"
        class="name">
            {{ edu.thesis.name[lang] }}
        </div>
        <div class="info" v-if="thesisShown">
            <div class="title">
                <span>{{ edu.thesis.titleName[lang] }}: </span>
                <span class="title">{{ edu.thesis.title[lang] }}</span>
            </div>
            <div class="supervisor">
            <span class="title">{{ edu.thesis.supervisor.title[lang] }}: </span>
            <span class="name">{{ edu.thesis.supervisor.name[lang] }}, </span>
            <span class="degree">{{ edu.thesis.advisor.degree[lang] }}</span>
            </div>
            <div class="advisor">
            <span class="title">{{ edu.thesis.advisor.title[lang] }}: </span>
            <span class="name">{{ edu.thesis.advisor.name[lang] }}, </span>
            <span class="degree">{{ edu.thesis.advisor.degree[lang] }}</span>
            </div>
            <div class="reviewer">
            <span class="title">{{ edu.thesis.reviewer.title[lang] }}: </span>
            <span class="name">{{ edu.thesis.reviewer.name[lang] }}, </span>
            <span class="degree">{{ edu.thesis.advisor.degree[lang] }}</span>
            </div>
            <div class="grades">
            <div class="supervisor">{{ edu.thesis.grades.supervisor[lang] }}</div>
            <div class="reviewer">{{ edu.thesis.grades.reviewer[lang] }}</div>
            <div class="board">{{ edu.thesis.grades.board[lang] }}</div>
            </div>
        </div>
      </div>
</template>

<script>
export default {
  name: 'EduThesisInfo',
  inject: ['lang'],
  props: {
    lang: String,
    edu: Object
  },
  data () {
    return {
      thesisShown: false
    }
  },
  methods: {
    showThesisInfo () {
      this.thesisShown = !this.thesisShown
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";

.thesis {
    margin-top: 1em;
    >.name {
        font-weight: 500;
        margin-bottom: .5em;
        text-decoration: underline;
        &:hover {
            cursor: pointer;
        }
    }
}

.info {
    margin: 0 1em;
}

.title {
    span.title {
        font-weight: 600;
    }
}

.title, .supervisor, .advisor, .reviewer{
    line-height: 1.5em;
}

.grades {
    margin: .5em 0;
    font-size: .9em;
}

.supervisor>.name,
.advisor>.name,
.reviewer>.name {
    font-weight: 600;
}
</style>
