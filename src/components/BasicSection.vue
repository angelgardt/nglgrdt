<template>
    <div class="basic">
        <div class="photo">
            <img src="@/assets/photo.png" alt="">
        </div>
        <div class="info">
            <h1>{{ basic.name }}</h1>
            <div class="city-age">
                <span>{{ basic.city }}</span>, <span>{{ calcAge() }}</span> y. o.
            </div>
            <div class="contacts">
                <div
                v-for="contact in basic.contacts"
                :key="contact">
                    <div>{{ contact.value }}</div>
                </div>
            </div>
            <div class="current-job">
                <div
                v-for="job in basic.currentJob"
                :key="job">
                    <div v-if="job">
                        <div class="position">{{ job.position }}</div>
                        <div class="organization">{{ job.organization }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BasicSectionJSON from '@/content/BasicSection.json'

export default {
  name: 'BasicSection',
  data () {
    return {
      basic: BasicSectionJSON
    }
  },
  methods: {
    calcAge () {
      return new Date(new Date() - new Date(this.basic.birth)).getUTCFullYear() - 1970
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";

.photo img {
    width: 15em;
    margin-right: 2em;
}

.basic {
    margin: auto;
    margin-top: 2em;
    text-align: center;
    div {
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
