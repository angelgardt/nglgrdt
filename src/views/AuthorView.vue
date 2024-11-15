<template>
  <nav class="nav-secondary">
        <a
        v-for="(section, idx) in Content"
        :key="idx"
        href="">
          {{ section.SectionTitle[lang] }}
        </a>
    </nav>
  <BasicSection
  :lang="lang"/>
  <div class="section"
  v-for="(section, idx) in Content"
  :key="idx">
    <h2>{{ section.SectionTitle[lang] }}</h2>
    <div
    v-if="section.subsections">
      <div
      v-for="(subsection, idx) in section.SectionContent"
      :key="idx">
        <h3>{{ subsection.SubsectionTitle[lang] }}</h3>

      </div>
    </div>
    <div v-else>
      <div
      v-if="section.SectionType === 'items'">
        items
      </div>
      <div
      v-if="section.SectionType === 'bubbles'">
        <div
        v-for="(bubble, idx) in section.SectionContent"
        :key="idx">
          {{ bubble }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BasicSection from '@/components/BasicSection.vue'
import BasicInfoJSON from '@/content/cv/BasicInfo.json'
import ContentJSON from '@/content/cv/Content.json'

export default {
  name: 'cvView',
  props: {
    lang: String
  },
  data () {
    return {
      BasicInfo: BasicInfoJSON,
      Content: ContentJSON
    }
  },
  components: {
    BasicSection
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";

nav.nav-secondary {
    a {
        display: inline-block;
        padding: 1em 1em;
        font-weight: 400;
        color: $tintedblack;
        text-transform: lowercase;
        &:hover {
            background-color: $shadedwhite;
        }
    }
}
</style>
