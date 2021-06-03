<template>
  <div>
    <h4>Give us the name of your favorite beer we'll recommend you some beers you're sure to like!</h4>
    <h4>Please enter at least one beer name to get a recommendation.</h4><br><br>

    <form class="recform" name="recform" @submit.prevent="processForm">

      <p>Name(s) of your favorite beer(s)</p>
      <div class="form-field">
        <vue-tags-input
            id="beer_name" name="beer_name" placeholder="ex. Sausa Weizen, Bud Light"
            v-model="tag"
            :tags="tags"
            :autocomplete-items="autocompleteItems"
            :add-only-from-autocomplete="true"
            @tags-changed="update" style="width: 100%; color: #000000;"
        />
      </div>

      <button type="submit" class="submit-button">Submit</button>
    </form>
  </div>
</template>

<script>
import VueTagsInput from '@johmun/vue-tags-input';
import axios from "axios";
// import axios from 'axios';

export default {
  name: 'BeerRecForm',
  components: {
    VueTagsInput
  },
  data() {
    return {
      tag: '',
      tags: [],
      autocompleteItems: [],
      debounce: null,
      errors: [],
    };
  },
  watch: {
    'tag': 'initItems',
  },
  mounted() {
  },
  methods: {

    processForm() {

      var beers = this.$store.state.beerNames;
      var selectedBeers = [];

      this.tags.forEach(t => {
        var selectedBeer = beers.find(x => x.beer_name.toLowerCase() == t.text.toLowerCase());
        if (selectedBeer) {
          selectedBeers.push(selectedBeer);
        }
      });

      this.$store.state.selectedBeers = selectedBeers;
      //this.$store.state.selectedABV = Number(document.getElementById('abv').value);

      if (this.$store.state.selectedBeers.length == 0) {
        alert("Please enter at least one beer.");
        return false;
      }

      let promises = [];
      let selectedBeersNames = [];
      this.$store.state.selectedBeers.forEach(beer => {
        selectedBeersNames.push(beer.beer_name);
      });
      const url = `/api/recommendation`
      let recommendationRequest = {beer_names: selectedBeersNames, n: 5};
      promises.push(axios.post(url, recommendationRequest));

      let recommendedBeerNames = [];
      let recommendedBeers = [];

      Promise.all(promises)
          .then((results) => {
            if (results && results.length > 0) {
              results.forEach((result) => {
                if (result.data.length > 0) {
                  recommendedBeerNames = recommendedBeerNames.concat(result.data);
                }
              });
            }
          })
          .then(() => {
            recommendedBeerNames = [...new Set(recommendedBeerNames)];

            recommendedBeerNames.forEach(beerName => {
              var recBeer = beers.find(x => x.beer_name.toLowerCase() == beerName.toLowerCase());
              if (recBeer) {
                recommendedBeers.push(recBeer);
              }
            });

            this.$store.state.recommendedBeers = recommendedBeers;
            this.$router.push('/rate');
          })
          .catch((error) => {
            console.log(error);
          });
    },
    update(newTags) {
      this.autocompleteItems = [];
      this.tags = newTags;
    },
    initItems() {
      if (this.tag.length < 2) return;

      clearTimeout(this.debounce);
      this.debounce = setTimeout(() => {
        var beers = this.$store.state.beerNames;
        if (beers) {
          this.autocompleteItems = beers
              .filter((x) => {
                return x.beer_name.toLowerCase().includes(this.tag.toLowerCase());
              })
              .map((x) => {
                return {text: x.beer_name};
              });
        }
      }, 600);
    },
  },
};
</script>

<style scoped lang="scss">

.recform {
    height: 66ch;
    position: relative;
    display: block;
}

.submit-button {
  background-color: #F5606D;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  bottom: 0px;
  right: 178px;
  position: absolute;
}

</style>