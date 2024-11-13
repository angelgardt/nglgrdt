<template>
    <div class="basic">
        <div class="photo">
            <img src="@/assets/photo.png" alt="">
        </div>
        <div class="info">
            <h1>{{ basic.name[lang] }}</h1>
            <div class="city-age">
                <span>{{ basic.city[lang] }}</span>, <span>{{ calcAge() }}</span> <span>{{ ageName() }}</span>
            </div>
            <div class="contacts">
                <div
                class="contact"
                v-for="(contact, key, idx) in basic.contacts"
                :key="idx">
                    <a v-if="contact.show"
                    :href="contact.link"
                    target="_blank">
                        <img
                        :src="require(`@/assets/icons/${key}.svg`)"
                        :alt="key"/>
                    </a>
                </div>
            </div>
            <div class="current-job">
                <div
                v-for="job in basic.currentJob"
                :key="job">
                    <div v-if="job">
                        <div class="position">{{ job.position[lang] }}</div>
                        <div class="organization">{{ job.organization[lang] }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BasicSectionJSON from '@/content/cv/BasicSection.json'

export default {
  name: 'BasicSection',
  props: {
    lang: String
  },
  data () {
    return {
      basic: BasicSectionJSON,
      contactIconURL: '@/assets/icons/'
    }
  },
  methods: {
    calcAge () {
      return new Date(new Date() - new Date(this.basic.birth.date)).getUTCFullYear() - 1970
    },
    ageName () {
      if (this.lang === 'ru') {
        if (this.calcAge() % 10 === 0) {
          return this.basic.birth.ru[0]
        } else if (this.calcAge() % 10 > 4) {
          return this.basic.birth.ru[0]
        } else if (this.calcAge() % 100 > 10 && this.calcAge() % 100 < 15) {
          return this.basic.birth.ru[0]
        } else if (this.calcAge() % 10 > 1 && this.calcAge() % 10 < 5) {
          return this.basic.birth.ru[1]
        } else {
          return this.basic.birth.ru[2]
        }
      } else {
        return this.basic.birth[this.lang]
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";

.photo img {
    width: 15em;
    margin-right: 2em;
}

.basic {
    margin: auto;
    margin-top: 2em;
    margin-bottom: 2em;
    text-align: center;
    &>div {
        display: inline-block;
        vertical-align: middle;
        margin: 0;
    }
    .info {
        div {
            display: block;
            margin: 0;
            text-align: left;
        }
        .contacts {
            display: flex;
            margin: 1em 0;
            >.contact {
                margin-right: .5em;
                img {
                    width: 2em;
                }
            }
        }
        .current-job {
            &>div {
                margin: .5em 0;
            .position {
                font-weight: 600;
            }
            .organization {
                font-weight: 400;
            }
            }
        }
    }
}
</style>
