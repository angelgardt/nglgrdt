<template>
    <div class="item"
    v-for="(item, idx) in items"
    :key="idx">
        <div class="item-title"
        v-if="item.position">
            {{ item.position[lang] }}
        </div>
        <div class="item-date"
        v-if="item.years">
            {{ item.years }}
        </div>
        <div class="item-title"
        v-if="item.uni">
            {{ item.uni[lang] }}
        </div>
        <div class="item-title"
        v-if="item.title">
            {{ item.title[lang] }}
        </div>
        <div class="item-caption"
        v-if="item.caption">
            {{ item.caption[lang] }}
        </div>
        <div class="item-subtitle"
        v-if="item.company">
            {{ item.company[lang] }}
        </div>
        <div class="item-subtitle"
        v-if="item.subtitle">
            {{ item.subtitle[lang] }}
        </div>
        <div class="item-subtitle"
        v-if="item.faculty">
            {{ item.faculty[lang] }}
        </div>
        <div class="item-subtitle"
        v-if="item.program">
            {{ item.program[lang] }}
        </div>
        <div class="item-caption"
        v-if="item.spec">
            {{ item.spec[lang] }}
        </div>
        <div class="item-caption"
        v-if="item.field">
            {{ item.field[lang] }}
        </div>
        <div class="item-gpa"
        v-if="item.gpa">
            {{ item.gpa }}
        </div>
        <div class="minor"
        v-if="item.minor">
            <div class="item-header">{{ item.minor.header[lang] }}</div>
            <div class="item-subtitle">{{ item.minor.faculty[lang] }}</div>
            <div class="item-subtitle">{{ item.minor.program[lang] }}</div>
            <div class="item-caption">{{ item.minor.field[lang] }}</div>
        </div>
        <ThesisInfo
        v-if="item.thesis"
        :lang="lang"
        :thesis="item.thesis"/>
        <div class="item-subtitle"
        v-if="item.org">
            {{ item.org[lang] }}
        </div>
        <div class="item-caption"
        v-if="item.platform || item.author || item.uni">
            <span v-if="item.author">{{ item.author[lang] }}</span>
            <span v-if="item.author && item.org"> | </span>
            <span v-if="item.org">{{ item.org[lang] }}</span>
            <span v-if="(item.org || item.author) && item.platform"> | </span>
            <span v-if="item.platform">{{ item.platform[lang] }}</span>
        </div>
        <div class="subtitle"
        v-if="item.report">
            {{ item.report[lang] }}
        </div>
        <div class="item-date"
        v-if="item.duration">
            {{ item.duration[lang] }}
        </div>
        <div v-if="item.place">
            {{ item.place[lang] }}
        </div>
        <div class="item-date"
        v-if="item.date">
            {{ item.date[lang] }}
        </div>
        <div class="item-description"
        v-if="item.description">
            {{ item.description[lang] }}
        </div>
        <div class="item-details"
        v-if="item.details">
            <div>{{ item.details.title[lang] }}</div>
            <div
            v-for="(line, idx) in item.details.content"
            :key="idx">
                <span>{{ line[lang][0] }}</span>&nbsp;
                <span>{{ line[lang][1] }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import ThesisInfo from './ThesisInfo.vue'

export default {
  name: 'ItemComp',
  props: {
    lang: String,
    items: Object
  },
  components: {
    ThesisInfo
  }
}
</script>
