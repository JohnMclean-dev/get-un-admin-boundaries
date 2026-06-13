-- Uncomment to delete table
DROP TABLE IF EXISTS public.gadm_410_simplified;

-- Create new table
CREATE TABLE IF NOT EXISTS public.gadm_410_simplified AS

SELECT

	-- Boundary Level Identifier
	gid_0,
	gid_1,
	gid_2,
	gid_3,
	gid_4,
	gid_5,

	-- Names
	ANY_VALUE(name_0) AS name_0,
	ANY_VALUE(name_1) AS name_1,
	ANY_VALUE(name_2) AS name_2,
	ANY_VALUE(name_3) AS name_3,
	ANY_VALUE(name_4) AS name_4,
	ANY_VALUE(name_5) AS name_5,
	
	-- Classifications
	'Country' AS class_0,
	ANY_VALUE(engtype_1) AS class_1,
	ANY_VALUE(engtype_2) AS class_2,
	ANY_VALUE(engtype_3) AS class_3,
	ANY_VALUE(engtype_4) AS class_4,
	ANY_VALUE(engtype_5) AS class_5,
	
	-- Governance
	sovereign,
	LOWER(sovereign) = LOWER(ANY_VALUE(name_0)) AS is_sovereign,
	CASE
		WHEN LOWER(continent) IN ('australia', 'oceania') THEN 'Oceania'
		ELSE continent
	END AS continent,

	-- Geometry
	ST_UNION(geom) as geom

FROM public.gadm_410

WHERE
	-- Water body classifiations
	NOT (
		LOWER(engtype_1) ~* 'water' OR 
		LOWER(engtype_2) ~* 'water' OR 
		LOWER(engtype_3) ~* 'water' OR 
		LOWER(engtype_4) ~* 'water' OR 
		LOWER(engtype_5) ~* 'water'
	
	)

	-- Ignore the Caspian Sea
	AND NOT gid_0 = 'XCA'

	-- Ignore Antarctica
	AND NOT LOWER(continent) = 'antarctica'
	
GROUP BY
	gid_0,
	gid_1,
	gid_2,
	gid_3,
	gid_4,
	gid_5,
	sovereign,
	continent;
