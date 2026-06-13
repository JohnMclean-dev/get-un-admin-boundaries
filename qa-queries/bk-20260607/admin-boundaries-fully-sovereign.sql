
-- Uncomment to delete table
DROP TABLE IF EXISTS public.global_admin_boundaries_fully_sovereign;

-- Create new table
CREATE TABLE IF NOT EXISTS public.global_admin_boundaries_fully_sovereign AS

WITH global_admin_boundaries_lvl_1_sub AS (

    SELECT
        sovereignty_of,
        ST_Union(geom) AS geom
    
    FROM public.global_admin_boundaries_lvl_1

    GROUP BY
        sovereignty_of

)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY
            sovereignty_of
    ) AS this_uid,

    *

FROM global_admin_boundaries_lvl_1_sub;
