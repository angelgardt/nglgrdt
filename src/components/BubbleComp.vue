<template>
    <div class="bubble-wrapper">
        <div class="bubble"
        v-for="(bubble, idx) in bubbles"
        :key = "idx">
        {{ bubble }}
    </div>
    </div>
</template>

<script>
export default {
  name: 'BubbleComp',
  props: {
    bubbles: Object,
    align: String
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";
</style>
