DROP TABLE IF EXISTS public.districts;

CREATE TABLE public.districts AS

WITH base AS (
    SELECT

        -- flatten arrays only once per district group
        ARRAY_AGG(DISTINCT continent ORDER BY continent) AS continents,

        sovereign AS nation,

        gid_0 AS country_id,
        name_0 AS country,

        COALESCE(LOWER(TRIM(sovereign)), '')
        = COALESCE(LOWER(TRIM(name_0)), '') AS is_sovereign,

        gid_1 AS region_id,
        name_1 AS region,
        engtype_1 AS region_class,

        gid_2 AS district_id,
        name_2 AS district,
        engtype_2 AS district_class,

        ST_UNION(geom) AS geom

    FROM public.gadm_410

    GROUP BY
        sovereign,
        gid_0,
        name_0,
        gid_1,
        name_1,
        engtype_1,
        gid_2,
        name_2,
        engtype_2
),

final AS (
    SELECT
        nation,
        country_id,
        country,
        is_sovereign,
        region_id,
        region,
        region_class,
        district_id,
        district,
        district_class,

        -- sort only once at the end (cheaper than per-group ORDER BY inside aggregate)
        ARRAY(
            SELECT DISTINCT unnest(continents)
            ORDER BY 1
        ) AS continents,

        geom
    FROM base
)

SELECT    
	ROW_NUMBER() OVER (ORDER BY nation, country, region, district) AS this_uid,
    *

FROM final;