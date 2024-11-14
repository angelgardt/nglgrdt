<template>
    <div class="item">
        <div class="item-title"
        v-if="title">
            {{ title }}
        </div>
        <div class="item-caption"
        v-if="caption">
            {{ caption }}
        </div>
        <div class="item-caption"
        v-if="platform && author">
            <span>{{ author }}</span> | <span>{{ platform }}</span>
        </div>
        <div class="item-subtitle"
        v-if="subtitle">
            {{ subtitle }}
        </div>
        <div class="item-date"
        v-if="date">
            {{ date }}
        </div>
    </div>
</template>

<script>
export default {
  name: 'ItemComp',
  props: {
    title: String,
    caption: String,
    subtitle: String,
    author: String,
    platform: String,
    date: String
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/style.scss";

.item {
    background-color: $almostwhite;
}
</style>
