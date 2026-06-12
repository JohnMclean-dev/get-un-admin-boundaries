
-- Uncomment to delete table
DROP TABLE IF EXISTS public.gadm_410_simplified_region;

-- Create new table
CREATE TABLE IF NOT EXISTS public.gadm_410_simplified_region AS
SELECT
	gid_0,
	gid_1,

	sovereign,
	ANY_VALUE(name_0) AS name_0,
	ANY_VALUE(name_1) AS name_1,

	ANY_VALUE(class_0) AS class_0,
	ANY_VALUE(class_1) AS class_1,

	ST_UNION(geom) AS geom

FROM public.gadm_410_simplified

GROUP BY gid_0, gid_1, sovereign;
