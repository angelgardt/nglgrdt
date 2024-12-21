<template>
    <div class="item">
        <p v-if="pub.type == 'article'">
            <span v-if="pub.author[lang]">{{ pub.author[lang] }}&ensp;</span>
            <span v-if="pub.year[lang]">({{ pub.year[lang] }}).&ensp;</span>
            <span v-if="pub.title[lang]">{{ pub.title[lang] }}&ensp;</span>
            <span v-if="pub.journal[lang]"><em>{{ pub.journal[lang] }}</em>,&ensp;</span>
            <span v-if="pub.volume[lang]"><em>{{ pub.volume[lang] }}</em></span>
            <span v-if="pub.number[lang]">({{ pub.number[lang] }}),&ensp;</span>
            <span v-else>,&ensp;</span>
            <span v-if="pub.pages[lang]">{{ pub.pages[lang] }}.&ensp;</span>
            <span v-if="pub.doi">https://doi.org/{{ pub.doi }}</span>
        </p>
    </div>
</template>

<script>
export default {
  name: 'PubComp',
  props: {
    lang: String,
    pub: Object
  }
}
</script>

<style lang="scss" scoped>
.item > p {
    margin: 0;
    padding-left: 5em;
    text-indent: -5em;
    line-height: 1.5;
}
</style>
