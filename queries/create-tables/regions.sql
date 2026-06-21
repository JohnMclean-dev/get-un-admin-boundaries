DROP TABLE IF EXISTS public.regions;

CREATE TABLE public.regions AS

WITH base AS (
    SELECT
        d.nation,
        d.country_id,
        d.country,
        d.is_sovereign,

        d.region_id,
        d.region,
        d.region_class,

        -- flatten directly without extra CTEs
        ARRAY_AGG(DISTINCT c.continent ORDER BY c.continent) AS continents,

        ST_UNION(d.geom) AS geom

    FROM public.districts d
    CROSS JOIN LATERAL UNNEST(d.continents) AS c(continent)

    GROUP BY
        d.nation,
        d.country_id,
        d.country,
        d.is_sovereign,
        d.region_id,
        d.region,
        d.region_class
)

SELECT
    ROW_NUMBER() OVER (ORDER BY nation, country, region) AS this_uid,
    *
FROM base;