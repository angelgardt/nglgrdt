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

.bubble-wrapper {
    text-align: v-bind(align)
}
.bubble {
    margin: .5em;
    padding: .5em;
    display: inline-block;
    background-color: $almostwhite;
    border: 1px solid $almostblack;
    border-radius: 10px;
}
</style>
