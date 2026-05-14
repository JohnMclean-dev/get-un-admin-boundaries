-- Define the search parameter values once so they can be changed without editing the main query.
WITH params AS (
    SELECT
		-- User location
        -80.312346::double precision AS lon,
        43.377252::double precision AS lat,
        -- Radius expressed in degrees for the current approximation.
        0.4::double precision AS radius_deg
),

-- Build the user location point in WGS84 (SRID 4326).
user_pt AS (
    SELECT
        ST_SetSRID(ST_Point(p.lon, p.lat), 4326) AS geom
    FROM params p
)

-- Search for geometries within the specified radius around the user point.
-- In this query, radius is supplied in approximate degrees.
SELECT DISTINCT
	-- g.fid,
    g.uid,

    g.gid_0,
    g.name_0,
    -- g.varname_0,

    g.gid_1,
    g.name_1,
    -- g.varname_1,
    -- g.nl_name_1,
    g.iso_1,
    g.hasc_1,
    g.cc_1,
    -- g.type_1,
    g.engtype_1,
    -- g.validfr_1,

    g.gid_2,
    g.name_2,
    -- g.varname_2,
    -- g.nl_name_2,
    g.hasc_2,
    g.cc_2,
    -- g.type_2,
    g.engtype_2,
    -- g.validfr_2,

    g.gid_3,
    g.name_3,
    -- g.varname_3,
    -- g.nl_name_3,
    g.hasc_3,
    g.cc_3,
    -- g.type_3,
    g.engtype_3,
    -- g.validfr_3,

    g.gid_4,
    g.name_4,
    -- g.varname_4,
    g.cc_4,
    -- g.type_4,
    g.engtype_4,
    -- g.validfr_4,

    g.gid_5,
    g.name_5,
    g.cc_5,
    -- g.type_5,
    g.engtype_5,

    g.governedby,
    g.sovereign,
    -- g.disputedby,

    g.region,
    -- g.varregion,
    g.country,
    g.continent,
    -- g.subcont,

    g.geom

FROM public.gadm_410 g, user_pt u, params p
WHERE ST_DWithin(g.geom, u.geom, p.radius_deg)
ORDER BY uid ASC;