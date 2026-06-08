
-- Uncomment to delete table
DROP TABLE IF EXISTS public.sovereign_gid_lkp;

-- Create new table
CREATE TABLE IF NOT EXISTS public.sovereign_gid_lkp AS

WITH soverign_nations AS (

	SELECT DISTINCT
		sovereign
	
	FROM public.gadM_410_simplified

), soverign_nations_gid_lkp AS (

	SELECT DISTINCT
		a.gid_0 as sovereign_gid,
		b.sovereign as sovereign

	FROM public.gadM_410_simplified AS a

	INNER JOIN soverign_nations AS b
		ON LOWER(a.sovereign) = LOWER(b.sovereign)

	WHERE a.is_sovereign
	
)

SELECT * FROM soverign_nations_gid_lkp;
