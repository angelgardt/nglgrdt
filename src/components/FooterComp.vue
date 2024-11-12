<template>
  <footer>
    <div class="title">Anton Angelgardt</div>
    <div class="email">anton.angelgardt@gmail.com</div>
    <div class="years">2020–<span>{{ currentYear() }}</span></div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComp',
  methods: {
    currentYear () {
      return new Date().getFullYear()
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";

footer {
  padding: 1em;
  margin-top: 2em;
  background-color: $almostblack;
  color: $darkgray;
}
.title, .email {
  padding: .1em 0;
}

.years{
  padding:  1em 0;
}
</style>
