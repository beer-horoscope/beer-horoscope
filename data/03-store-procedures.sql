DELIMITER //

CREATE PROCEDURE post_beer_rating (
    IN p_beer_name varchar(128),
    IN p_review_overall int
)
BEGIN
    -- specified input fields
    DECLARE v_beer_name varchar(128);
    DECLARE v_review_overall int;
    DECLARE v_review_profilename varchar(128);

    -- calculated input fields
    DECLARE v_review_time bigint;
    
    -- derived input fields
    DECLARE v_brewery_id int;
    DECLARE v_beer_style varchar(128);
    DECLARE v_brewery_name varchar(128);
    DECLARE v_review_aroma int;
    DECLARE v_review_appearance int;
    DECLARE v_review_palate int;
    DECLARE v_review_taste int;
    DECLARE v_beer_abv varchar(64);
    DECLARE v_beer_beerid int;

    SET v_beer_name = p_beer_name;
    SET v_review_overall = p_review_overall;
    SET v_review_aroma = 0;
    SET v_review_appearance = 0;
    SET v_review_palate = 0;
    SET v_review_taste = 0;
    SET v_review_time = unix_timestamp();
    SET v_review_profilename = UUID();

    SELECT DISTINCT
        brewery_id, 
        beer_style,
        brewery_name,
        beer_abv,
        beer_beerid
    INTO
        v_brewery_id, 
        v_beer_style,
        v_brewery_name,
        v_beer_abv,
        v_beer_beerid   
    FROM beer_reviews
    WHERE LOWER(beer_name) = LOWER(p_beer_name);

	INSERT INTO beer_reviews
    (
	  brewery_id,
	  brewery_name,
	  review_time,
	  review_overall,
	  review_aroma,
	  review_appearance,
	  review_profilename,
	  beer_style,
	  review_palate,
	  review_taste,
	  beer_name,
	  beer_abv,
	  beer_beerid
    )
    VALUES
    (
	  v_brewery_id,
	  v_brewery_name,
	  v_review_time,
	  v_review_overall,
	  v_review_aroma,
	  v_review_appearance,
	  v_review_profilename,
	  v_beer_style,
	  v_review_palate,
	  v_review_taste,
	  v_beer_name,
	  v_beer_abv,
	  v_beer_beerid
    );
END