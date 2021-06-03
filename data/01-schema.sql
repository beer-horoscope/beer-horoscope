CREATE SCHEMA `beer_horoscope` ;

CREATE TABLE `beer_reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brewery_id` int NOT NULL,
  `brewery_name` varchar(128) NOT NULL,
  `review_time` bigint DEFAULT NULL,
  `review_overall` int DEFAULT NULL,
  `review_aroma` int DEFAULT NULL,
  `review_appearance` int DEFAULT NULL,
  `review_profilename` varchar(128) DEFAULT NULL,
  `beer_style` varchar(128) DEFAULT NULL,
  `review_palate` int DEFAULT NULL,
  `review_taste` int DEFAULT NULL,
  `beer_name` varchar(128) DEFAULT NULL,
  `beer_abv` varchar(64) DEFAULT NULL,
  `beer_beerid` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2317 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
