DROP TABLE IF EXISTS public.countries;

CREATE TABLE public.countries AS

WITH base AS (
    SELECT
        nation,
        country_id,
        country,

        BOOL_AND(is_sovereign) AS is_sovereign,

        -- flatten arrays only once per region, not per row explosion
        ARRAY_AGG(DISTINCT c.continent) AS continents,

        ST_UNION(geom) AS geom

    FROM public.regions r
    CROSS JOIN LATERAL UNNEST(r.continents) AS c(continent)

    GROUP BY
        nation,
        country_id,
        country
),

final AS (
    SELECT
        nation,
        country_id,
        country,
        is_sovereign,

        -- sort only once at the end (cheaper than per-group ORDER BY inside aggregate)
        ARRAY(
            SELECT DISTINCT unnest(continents)
            ORDER BY 1
        ) AS continents,

        geom
    FROM base
)

SELECT
    ROW_NUMBER() OVER (ORDER BY nation, country) AS this_uid,
    *
FROM final;