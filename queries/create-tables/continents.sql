DROP TABLE IF EXISTS public.continents;

CREATE TABLE public.continents AS
WITH base AS (
    SELECT
        continent,
        ARRAY_AGG(DISTINCT sovereign ORDER BY sovereign ASC) AS nations,
        ST_UNION(geom) AS geom
    FROM public.gadm_410
    GROUP BY continent
)
SELECT
    ROW_NUMBER() OVER (ORDER BY continent) AS this_uid,
    *
FROM base;