<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
  <div>
    Anton Angelgardt
  </div>
  <EducationMain/>
</template>

<script>
import EducationMain from '@/components/EducationMain.vue'

export default {
  name: 'AuthorView',
  components: {
    EducationMain
  }
}

</script>
