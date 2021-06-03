LOAD DATA LOCAL INFILE '/var/lib/mysql-files/beer_reviews.csv' 
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