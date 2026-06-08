
-- Uncomment to delete table
DROP TABLE IF EXISTS public.global_admin_boundaries_lvl_3;

-- Create new table
CREATE TABLE IF NOT EXISTS public.global_admin_boundaries_lvl_3 AS

WITH global_admin_boundaries_lvl_4_sub AS (

    SELECT
        sovereignty_of,

        lvl_1_boundary_id,
        ANY_VALUE(lvl_1_boundary_name) AS lvl_1_boundary_name,
        ANY_VALUE(lvl_1_classification) AS lvl_1_classification,

        lvl_2_boundary_id,
        ANY_VALUE(lvl_2_boundary_name) AS lvl_2_boundary_name,
        ANY_VALUE(lvl_2_classification) AS lvl_2_classification,

        lvl_3_boundary_id,
        ANY_VALUE(lvl_3_boundary_name) AS lvl_3_boundary_name,
        ANY_VALUE(lvl_3_classification) AS lvl_3_classification,

        ST_Union(geom) AS geom
    
    FROM public.global_admin_boundaries_lvl_4

    GROUP BY
        sovereignty_of,
        lvl_1_boundary_id,
        lvl_2_boundary_id,
        lvl_3_boundary_id

)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY
            sovereignty_of,
            lvl_1_boundary_id,
            lvl_2_boundary_id,
            lvl_3_boundary_id
    ) AS this_uid,

    *

FROM global_admin_boundaries_lvl_4_sub;
