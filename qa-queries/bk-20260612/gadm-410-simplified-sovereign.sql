
-- Uncomment to delete table
DROP TABLE IF EXISTS public.gadm_410_simplified_sovereign;

-- Create new table
CREATE TABLE IF NOT EXISTS public.gadm_410_simplified_sovereign AS
SELECT
	sovereign,
	ST_UNION(geom) AS geom

FROM public.gadm_410_simplified

GROUP BY sovereign;
