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
