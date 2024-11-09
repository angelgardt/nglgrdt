<template>
  <div class="basic">
    <h1>Anton Angelgardt</h1>
    <div>
      <span>{{ city }}</span>, <span>{{ age }}</span> y. o.
    </div>
  </div>
  <EducationMain/>
  <CopyRights/>
</template>

<script>
import EducationMain from '@/components/EducationMain.vue'
import CopyRights from '@/components/CopyRights.vue'

export default {
  name: 'AuthorView',
  data () {
    return {
      city: 'Moscow',
      age: '27'
    }
  },
  components: {
    EducationMain,
    CopyRights
  }
}

</script>
