SET GLOBAL local_infile=1;

USE `beer_horoscope`;

-- LOAD DATA LOCAL INFILE 'update/the/path/to/beer_reviews.csv'
LOAD DATA LOCAL INFILE '/tmp/data/beer_reviews.csv' 
INTO TABLE beer_reviews 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(
  `brewery_id`,
  `brewery_name`,
  `review_time`,
  `review_overall`,
  `review_aroma`,
  `review_appearance`,
  `review_profilename`,
  `beer_style`,
  `review_palate`,
  `review_taste`,
  `beer_name`,
  `beer_abv`,
  `beer_beerid`
) set `id`=null;