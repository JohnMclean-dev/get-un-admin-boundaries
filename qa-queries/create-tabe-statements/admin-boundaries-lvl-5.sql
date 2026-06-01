
-- Uncomment to delete table
-- DROP TABLE IF EXISTS public.global_admin_boundaries_lvl_5;

-- Create new table
CREATE TABLE IF NOT EXISTS public.global_admin_boundaries_lvl_5 AS

WITH global_admin_boundaries_lvl_5_raw AS (

    SELECT
        sovereign AS sovereignty_of,

        gid_0 AS lvl_1_boundary_id,
        name_0 AS lvl_1_boundary_name,
        'Country' AS lvl_1_classification,

        gid_1 AS lvl_2_boundary_id,
        name_1 AS lvl_2_boundary_name,
        engtype_1 AS lvl_2_classification,

        gid_2 AS lvl_3_boundary_id,
        name_2 AS lvl_3_boundary_name,
        engtype_2 AS lvl_3_classification,

        gid_3 AS lvl_4_boundary_id,
        name_3 AS lvl_4_boundary_name,
        engtype_3 AS lvl_4_classification,

        gid_4 AS lvl_5_boundary_id,
        name_4 AS lvl_5_boundary_name,
        engtype_4 AS lvl_5_classification,

        geom

    FROM public.gadm_410

),

global_admin_boundaries_lvl_5_agg AS (

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

        lvl_4_boundary_id,
        ANY_VALUE(lvl_4_boundary_name) AS lvl_4_boundary_name,
        ANY_VALUE(lvl_4_classification) AS lvl_4_classification,

        lvl_5_boundary_id,
        ANY_VALUE(lvl_5_boundary_name) AS lvl_5_boundary_name,
        ANY_VALUE(lvl_5_classification) AS lvl_5_classification,

        -- ST_Collect(geom) AS geom
        ST_Union(geom) AS geom

    FROM global_admin_boundaries_lvl_5_raw

    GROUP BY
        sovereignty_of,
        lvl_1_boundary_id,
        lvl_2_boundary_id,
        lvl_3_boundary_id,
        lvl_4_boundary_id,
        lvl_5_boundary_id

)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY
            sovereignty_of,
            lvl_1_boundary_id,
            lvl_2_boundary_id,
            lvl_3_boundary_id,
            lvl_4_boundary_id,
            lvl_5_boundary_id
    ) AS this_uid,

    *
    
FROM global_admin_boundaries_lvl_5_agg;