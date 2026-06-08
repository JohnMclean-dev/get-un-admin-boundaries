
-- Uncomment to delete table
DROP TABLE IF EXISTS public.global_admin_boundaries_max_lvl;

-- Create new table
CREATE TABLE IF NOT EXISTS public.global_admin_boundaries_max_lvl AS

WITH max_lvl_5 AS (

	SELECT
		this_uid,
		sovereignty_of,

        5 as max_lvl_value,
        lvl_5_boundary_id as boundary_id,
        lvl_5_boundary_name as boundary_name,
        lvl_5_classification as classification,
        
        geom
		
	FROM public.global_admin_boundaries_lvl_5

	WHERE lvl_5_boundary_id != ''

), max_lvl_4 AS (

	SELECT
		this_uid,
		sovereignty_of,

        4 as max_lvl_value,
        lvl_4_boundary_id as boundary_id,
        lvl_4_boundary_name as boundary_name,
        lvl_4_classification as classification,
        
        geom

	FROM public.global_admin_boundaries_lvl_5

	WHERE
		lvl_4_boundary_id != '' AND
		lvl_5_boundary_id = ''

), max_lvl_3 AS (

	SELECT
		this_uid,
		sovereignty_of,

        3 as max_lvl_value,
        lvl_3_boundary_id as boundary_id,
        lvl_3_boundary_name as boundary_name,
        lvl_3_classification as classification,
        
        geom

	FROM public.global_admin_boundaries_lvl_5

	WHERE
		lvl_3_boundary_id != '' AND
		lvl_4_boundary_id = '' AND
		lvl_5_boundary_id = ''

), max_lvl_2 AS (

	SELECT
		this_uid,
		sovereignty_of,

        2 as max_lvl_value,
        lvl_2_boundary_id as boundary_id,
        lvl_2_boundary_name as boundary_name,
        lvl_2_classification as classification,
        
        geom

	FROM public.global_admin_boundaries_lvl_5

	WHERE
		lvl_2_boundary_id != '' AND
		lvl_3_boundary_id = '' AND
		lvl_4_boundary_id = '' AND
		lvl_5_boundary_id = ''

), max_lvl_1 AS (

	SELECT
		this_uid,
		sovereignty_of,

        1 as max_lvl_value,
        lvl_1_boundary_id as boundary_id,
        lvl_1_boundary_name as boundary_name,
        lvl_1_classification as classification,
        
        geom

	FROM public.global_admin_boundaries_lvl_5

	WHERE
		lvl_1_boundary_id != '' AND
		lvl_2_boundary_id = '' AND
		lvl_3_boundary_id = '' AND
		lvl_4_boundary_id = '' AND
		lvl_5_boundary_id = ''

)

SELECT * FROM max_lvl_1
UNION
SELECT * FROM max_lvl_2
UNION
SELECT * FROM max_lvl_3
UNION
SELECT * FROM max_lvl_4
UNION
SELECT * FROM max_lvl_5;
