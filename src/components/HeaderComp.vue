<template>
    <header>
        <div class="title">
            A. N. Angelgardt
        </div>
        <div class="subtitle">
            teacher, researcher, analyst
        </div>
    </header>
</template>

<script>
export default {
  name: 'HeaderComp'
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";

header {
    padding: 1em;
    text-align: center;
    vertical-align: top;
    background-color: $almostblack;
    color: $almostwhite;
}

.title {
    padding: .2em 0;
    font-size: 3em;
    font-weight: 700;
}

.subtitle {
    padding: .1em 0;
    font-size: 1.5em;
    font-weight: 200;
}
</style>
