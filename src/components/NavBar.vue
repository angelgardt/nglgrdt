<template>
    <nav class="nav-secondary">
        <a href="">work experience</a>
        <a href="">interests</a>
        <a href="">education</a>
        <a href="">additional education</a>
        <a href="">achievements</a>
        <a href="">language proficiency</a>
        <a href="">skillls</a>
        <a href="">research</a>
        <a href="">copyrights</a>
    </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped lang="scss">
@import "@/assets/variables.scss";

nav.nav-secondary {
    a {
        display: inline-block;
        padding: 1em 1em;
        font-weight: 400;
        color: $tintedblack;
        &:hover {
            background-color: $shadedwhite;
        }
    }
}
</style>
