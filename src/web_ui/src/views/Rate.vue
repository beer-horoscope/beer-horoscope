<template>
  <div className="rate">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <RatingPage></RatingPage>
  </div>
</template>

<script>
// @ is an alias to /src
import RatingPage from '@/components/RatingPage.vue'

export default {
  name: 'Rate',
  components: {
    RatingPage,
  }
}
</script>
