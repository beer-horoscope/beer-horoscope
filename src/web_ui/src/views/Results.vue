<template>
  <div className="results">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <ResultsPage></ResultsPage>
  </div>
</template>

<script>
// @ is an alias to /src
import ResultsPage from '@/components/ResultsPage.vue'

export default {
  name: 'Results',
  components: {
    ResultsPage,
  }
}
</script>
