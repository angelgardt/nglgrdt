<template>
    <h2>{{ header }}</h2>
    <div
    v-for="(subsec, key, idx) in WorkExp"
    :key="idx">
        <h3 v-if="subsec">{{ subheaders[key] }}</h3>
        <div class="item"
        v-for="(item, idx) in subsec"
        :key="idx">
            <div class="position">{{ item.position[lang] }}</div>
            <div class="company">{{ item.company[lang] }}</div>
            <div class="details"
            v-if="item.details">
                <div class="line"
                v-if="!(item.details.title)">
                {{ item.details[lang] }}
                </div>
            </div>
            <div class="duration">{{ item.duration[lang] }}</div>
            <div class="description">{{ item.description[lang] }}</div>
            <div class="details"
            v-if="item.details">
                <div class="list"
                v-if="item.details.title">
                    <div class="title">{{ item.details.title[lang] }}</div>
                    <ul>
                        <li
                        v-for="(li, idx) in item.details.content[lang]"
                        :key="idx">
                            <span v-if="li.c1" class="c1">{{ li.c1 }}</span>&nbsp;
                            <span v-if="li.c2" class="c2">{{ li.c2 }}</span>&nbsp;
                            <span v-if="li.c3" class="c3">{{ li.c3 }}</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import WorkExperienceJSON from '@/content/cv/WorkExperience.json'

export default {
  name: 'WorkExperience',
  props: {
    lang: String,
    header: String,
    subheaders: Object
  },
  data () {
    return {
      WorkExp: WorkExperienceJSON
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";

.item {
    .position, .company, .duration, .description {
        line-height: 1.5em;
    }
    .position {
        font-weight: 700;
    }
    .company {
        font-weight: 500;
    }
    .description {
        font-size: .9em;
    }
    .details {
        font-size: .9em;
        .title {
            font-weight: 500;
            padding: .5em 0;
        }
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0 .5em;
            li {
                line-height: 1.5em;
                .c2 {
                    color: $paleblack;
                }
            }
        }
    }
}
</style>
