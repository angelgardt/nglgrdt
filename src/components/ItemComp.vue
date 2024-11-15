<template>
    <div class="item"
    v-for="(item, idx) in items"
    :key="idx">
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
    lang: String,
    items: Object
  }
}
</script>
