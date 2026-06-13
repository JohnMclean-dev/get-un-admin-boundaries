
-- Uncomment to delete table
drop table if exists public.territories;

-- Create new table
create table if not exists public.territories as

select distinct

    row_number() over (

            order by
                continent asc, sovereign asc, name_0 asc, name_1 asc,
                name_2 asc, name_3 asc, name_4 asc, name_5 asc
        
        ) as this_uid,

    sovereign as nation,

    gid_0 as country_id,
    name_0 as country,

    gid_1 as region_id,
    name_1 as region,
    engtype_1 as region_type,

    gid_2 as district_id,
    name_2 as district,
    engtype_2 as district_type,

    gid_3 as community_id,
    name_3 as community,
    engtype_3 as community_type,

    gid_4 as area_id,
    name_4 as area,
    engtype_4 as area_type,

    gid_5 as territory_id,
    name_5 as territory,
    engtype_5 as territory_type,
    
    continent,

    st_area(st_unaryunion(st_collect(geom))::geography) as area_m2,
    st_union(geom) as geom

from public.gadm_410

where not (

        lower(engtype_1) ~* 'water' or 
        lower(engtype_2) ~* 'water' or 
        lower(engtype_3) ~* 'water' or 
        lower(engtype_4) ~* 'water' or 
        lower(engtype_5) ~* 'water'

    )

    -- Ignore the Caspian Sea
    and not gid_0 = 'XCA'

    -- Ignore Antarctica
    and not lower(continent) = 'antarctica'

group by

    sovereign, continent,
    gid_0, name_0,
    gid_1, name_1, engtype_1,
    gid_2, name_2, engtype_2,
    gid_3, name_3, engtype_3,
    gid_4, name_4, engtype_4,
    gid_5, name_5, engtype_5

order by this_uid;
