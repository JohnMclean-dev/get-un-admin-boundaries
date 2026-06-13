
-- Uncomment to delete table
DROP TABLE IF EXISTS public.global_admin_boundaries_lvl_1;

-- Create new table
CREATE TABLE IF NOT EXISTS public.global_admin_boundaries_lvl_1 AS

WITH global_admin_boundaries_lvl_2_sub AS (

    SELECT
        sovereignty_of,

        lvl_1_boundary_id,
        ANY_VALUE(lvl_1_boundary_name) AS lvl_1_boundary_name,
        ANY_VALUE(lvl_1_classification) AS lvl_1_classification,

        ST_Union(geom) AS geom
    
    FROM public.global_admin_boundaries_lvl_2

    GROUP BY
        sovereignty_of,
        lvl_1_boundary_id

)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY
            sovereignty_of,
            lvl_1_boundary_id
    ) AS this_uid,

    *

FROM global_admin_boundaries_lvl_2_sub;
