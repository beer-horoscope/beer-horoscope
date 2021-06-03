<template>
  <div id="app">
    <div class="header">
      <div class="logo"></div>
    </div>
    <div class="main-form">
      <div class="top-left-corner"></div>
      <div class="bottom-right-corner"></div>
      <div class="beer-bottle-one"></div>
      <div class="beer-bottle-two"></div>
      <router-view class="router"/>
    </div>

    <img src="../public/assets/rh-logo.png" class="rh_logo">
    <img src="../public/assets/datahub_color_hrz-gry-bg.png" class="odh_logo">
  </div>
</template>

<script>
import '../public/style.scss'
import axios from 'axios';

export default {
  name: 'Index',
  components: {},
  mounted() {
    const url = `/api/beer`
    axios.get(url)
        .then(response => {
          this.$store.state.beerNames = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
