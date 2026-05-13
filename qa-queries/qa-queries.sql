-- Assess column completeness by calculating the percentage of non-null and non-empty values for each column in the gadm_410 table.
SELECT
    column_name,
    COUNT(*) FILTER (
        WHERE val IS NOT NULL
          AND val !~ '^\s*$'
    ) * 1.0 / COUNT(*) AS pct_filled
FROM public.gadm_410 t
CROSS JOIN LATERAL jsonb_each_text(to_jsonb(t)) AS j(column_name, val)
GROUP BY column_name
ORDER BY pct_filled DESC, column_name ASC;

-- See simplified subquery of dataset
SELECT
	uid,
	
	gid_0,
	name_0,
	
	gid_1,
	name_1,
	type_1,
	
	gid_2,
	name_2,
	type_2,

	gid_3,
	name_3,
	type_3,

	gid_4,
	name_4,
	type_4,
	
	sovereign,
	country,
	continent,
	
	geom

FROM public.gadm_410

-- WHERE
-- 	type_4 IS NOT NULL AND type_4 <> ''

LIMIT 100;