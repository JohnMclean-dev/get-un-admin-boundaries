
-- Uncomment to delete table
DROP TABLE IF EXISTS public.gadm_410_simplified_area;

-- Create new table
CREATE TABLE IF NOT EXISTS public.gadm_410_simplified_area AS
SELECT
	gid_0,
	gid_1,
	gid_2,
	gid_3,

	sovereign,
	ANY_VALUE(name_0) AS name_0,
	ANY_VALUE(name_1) AS name_1,
	ANY_VALUE(name_2) AS name_2,
	ANY_VALUE(name_3) AS name_3,

	ANY_VALUE(class_0) AS class_0,
	ANY_VALUE(class_1) AS class_1,
	ANY_VALUE(class_2) AS class_2,
	ANY_VALUE(class_3) AS class_3,

	ST_UNION(geom) AS geom

FROM public.gadm_410_simplified

GROUP BY gid_0, gid_1, gid_2, gid_3, sovereign;
