<template>
    <div class="bubble-wrapper">
        <div class="bubble"
        v-for="(bubble, idx) in bubbles"
        :key="idx">
            <div
            v-if="bubble.show">
                <span v-if="bubble">{{ bubble[lang] }}</span>
                <span v-if="bubble.lang">{{ bubble.lang[lang] }}</span>
                <span v-if="bubble.level"> [{{ bubble.level[lang] }}]</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'BubbleComp',
  props: {
    lang: String,
    bubbles: Object,
    align: String
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";
</style>
