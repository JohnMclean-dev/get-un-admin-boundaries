
DROP TABLE IF EXISTS public.cities_districts_lkp;

CREATE TABLE IF NOT EXISTS public.cities_districts_lkp AS

WITH city_pts AS (

	SELECT
	
		continent_uid,
		city_uid,

		continent,
		city,
		
		city_class,
		city_rank,
		est_population,

		geom
	
	FROM public.cities_continents_lkp

), district_areas AS (

	SELECT
	
		this_uid AS district_uid,
		country_id,
		region_id,
		district_id,
		
		nation,
		country,
		region,
		district,

		is_sovereign,
		region_class,
		district_class,

		geom
	
	FROM public.districts
	
), base AS (

	SELECT

		continent_uid,
		district_uid,
		city_uid,
		country_id,
		region_id,
		district_id,

		continent,
		nation,
		country,
		region,
		district,
		city,

		is_sovereign,
		region_class,
		district_class,
		city_class,
		city_rank,
		est_population,

		c.geom

	FROM city_pts AS c

	LEFT JOIN district_areas AS d
		ON ST_WITHIN(c.geom, d.geom)

)

SELECT
	ROW_NUMBER() OVER (ORDER BY continent, nation, country, region, district, city) AS this_uid,
	*

FROM base;

