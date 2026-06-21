
DROP TABLE IF EXISTS public.cities_init;

CREATE TABLE IF NOT EXISTS public.cities_init AS

WITH base AS (

	SELECT

		-- Identifiers
		id AS worldcities_id,
		iso2,
		iso3,

		-- Names
		country,
		admin_name AS region,
		city,
		city_ascii,

		-- Categories and Data
		capital as city_class,
		CASE
			WHEN COALESCE(LOWER(TRIM(capital)), '') = 'primary' THEN 1
			WHEN COALESCE(LOWER(TRIM(capital)), '') = 'admin' THEN 2
			WHEN COALESCE(LOWER(TRIM(capital)), '') = 'minor' THEN 3
			ELSE 4
		END AS city_rank,
		population AS est_population,

		-- Geometry
		ST_POINT(lng, lat, 4326) AS geom

	FROM public.worldcities

)

SELECT
	ROW_NUMBER() OVER (ORDER BY country, region, city) AS this_uid,
	*

FROM base;

