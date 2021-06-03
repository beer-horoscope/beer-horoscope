<template>
  <div class="rating-container">
    <p>Rate a beer?</p>
    <p>The more beers you rate, the better our recommendations get!</p>

    <ul style="list-style-type: none" id="beer_rating">
      <li v-for="(beer, index) in this.$store.state.selectedBeers" :key="beer.beer_beerid" v-bind:item-id="beer.beer_beerid">
        <b><p>{{ beer.beer_name }}</p></b>
        <star-rating
            :key="index"
            :increment="0.1"
            class="rating-form"
            name="ratingNumber">
        </star-rating>
        <br/>
      </li>
    </ul>
    <button class="submit-button" @click="submitRating" type="submit">Submit</button>
    <br/>
    <br/>
    <router-link :to="{ name: 'Results'}">Take me directly to my horoscope</router-link>

  </div>
</template>

<script>
import axios from "axios";
import StarRating from 'vue-star-rating'

export default {
  name: "RatingPage",
  components: {
    StarRating
  },
  data() {
    return {
      ratings: []
    }
  },
  methods: {
    submitRating: function (){
      this.$store.state.selectedBeers.forEach(beer => {
        let itemSelectorQuery = "li[item-id='REPLACE'] .vue-star-rating-rating-text";
        itemSelectorQuery = itemSelectorQuery.replace('REPLACE', beer.beer_beerid);

        let rating = document.querySelector(itemSelectorQuery).innerText;
        const url = `/api/rating`
        var ratingRequest = {beer_name: beer.beer_name, review_overall: rating}
        axios.post(url, ratingRequest).catch((error) => {
          console.error(error);
        });
      });
      this.$router.push('/results');
    },
  },
}
</script>

<style scoped>
.rating-container {
  color: #ffffff;
}

.rating-form {
  position: relative;
  left: 75px;
}

.submit-button {
  background-color: #F5606D; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}
</style>