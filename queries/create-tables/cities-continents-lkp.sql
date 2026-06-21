
DROP TABLE IF EXISTS public.cities_continents_lkp;

CREATE TABLE IF NOT EXISTS public.cities_continents_lkp AS

WITH city_pts AS (

	SELECT
	
		this_uid AS city_uid,
		-- iso2,
		-- iso3,

		-- country,
		-- region,
		city,
		-- city_ascii,
		
		city_class,
		city_rank,
		est_population,

		geom
	
	FROM public.cities_init

), continent_areas AS (

	SELECT
	
		this_uid AS continent_uid,
		continent,
		geom
	
	FROM public.continents
	
), base AS (

	SELECT

		city_uid,
		continent_uid,

		continent,
		city,
		
		city_class,
		city_rank,
		est_population,

		c.geom

	FROM city_pts AS c

	LEFT JOIN continent_areas AS d
		ON ST_WITHIN(c.geom, d.geom)

)

SELECT
	ROW_NUMBER() OVER (ORDER BY continent, city) AS this_uid,
	*

FROM base;

