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
    <div
    v-if="section.show">
      <h2 class="wnav" v-if="section.subsections">{{ section.SectionTitle[lang] }}</h2>
      <h2 v-else>{{ section.SectionTitle[lang] }}</h2>

      <div
      v-if="section.subsections">
      <nav class="nav-tertiary">
        <a
        v-for="(subsection, idx) in section.SectionContent"
        :key="idx"
        href="">
          {{ subsection.SubsectionTitle[lang] }}
        </a>
      </nav>

        <div
        v-for="(subsection, idx) in section.SectionContent"
        :key="idx">
          <h3>{{ subsection.SubsectionTitle[lang] }}</h3>

          <div
          v-if="subsection.SubsectionID == 'pubs'">
            <div
            v-for="(pub, idx) in Pubs"
            :key="idx">
              <PubComp
              :pub="pub"
              :lang="lang"/>
            </div>
          </div>

          <div
          v-if="subsection.subsections">
            <div class="grid-container">
              <div
              v-for="(sub2section, idx) in subsection.SubsectionContent"
              :key="idx"
              >
                <h4>{{ sub2section.SubsectionTitle[lang] }}</h4>

                <div
                v-if="section.SectionType === 'items'">
                  <ItemComp
                  :items="sub2section.SubsectionContent"
                  :lang="lang"
                  />
                </div>
                <div
                v-if="section.SectionType === 'bubbles'">
                  <BubbleComp
                  :bubbles="sub2section.SubsectionContent"
                  :lang="lang"
                  :align="section.align"
                  />
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <div
            v-if="section.SectionType === 'items'">
              <ItemComp
              :items="subsection.SubsectionContent"
              :lang="lang"
              />
            </div>
            <div
            v-if="section.SectionType === 'bubbles'">
              <BubbleComp
              :bubbles="subsection.SubsectionContent"
              :lang="lang"
              :align="section.align"
              />
          </div>
        </div>

        </div>
      </div>

      <div
      v-else>
        <div
        v-if="section.SectionType === 'items'">
          <ItemComp
          :items="section.SectionContent"
          :lang="lang"
          />
        </div>
        <div
        v-if="section.SectionType === 'bubbles'">
          <BubbleComp
          :bubbles="section.SectionContent"
          :lang="lang"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BasicSection from '@/components/BasicSection.vue'
import BubbleComp from '@/components/BubbleComp.vue'
import ItemComp from '@/components/ItemComp.vue'
import PubComp from '@/components/PubComp.vue'
import BasicInfoJSON from '@/content/cv/BasicInfo.json'
import ContentJSON from '@/content/cv/Content.json'
import PubsJSON from '@/content/cv/Pubs.json'

export default {
  name: 'cvView',
  props: {
    lang: String
  },
  data () {
    return {
      BasicInfo: BasicInfoJSON,
      Content: ContentJSON,
      Pubs: PubsJSON.Pubs
    }
  },
  components: {
    BasicSection,
    BubbleComp,
    ItemComp,
    PubComp
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss"
</style>
