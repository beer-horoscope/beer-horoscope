<template>
  <div class="results-container">
    <br><br>
    <h4>Here is your horoscope:</h4>

    <table class="results-table">
      <tr class="title-row">
        <th>Beer Name</th>
        <th>Beer Style</th>
      </tr>
      <tr class="title-row">
        <th><br/></th>
        <th></th>
      </tr>
      <tr class="row" v-for="beer in this.$store.state.recommendedBeers" :key="beer.beer_beerid">
        <th>{{ beer.beer_name }}</th>
        <th>{{ beer.beer_style }}</th>
      </tr>
    </table>

    <br/>

    <router-link to="/">Go back</router-link>
  </div>
</template>

<script>
export default {
  name: "ResultsPage"
}
</script>

<style scoped lang="scss">
.results-container {
  color: #ffffff;
}

.results-table {
  position: relative;
  width: 100%;

  .title-row {
    font-weight: bold;

    th {
      padding: 10px;
      text-align: left;
      border: 1px solid;

    }
  }

  .row {
    font-weight: normal;

    th {
      padding: 10px;
      border: 1px solid;
      font-weight: normal;
      text-align: left;
    }
  }
}
</style>