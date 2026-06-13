
-- Uncomment to delete table
drop table if exists public.districts;

-- Create new table
create table if not exists public.districts as

select distinct

    row_number() over (order by min(this_uid)) as this_uid,
    nation,

    country_id,
    country,

    region_id,
    region,
    region_type,
    
    district_id,
    district,
    district_type,
    
    array_agg(distinct community_id order by community_id asc) filter (where community_id <> '') as community_ids,
    
    array_agg(distinct community order by community asc) filter (where community <> '') as communities,
    
    array_agg(distinct community_type order by community_type asc) filter (where community_type <> '') as community_types,
    
    
    array_agg(distinct continent order by continent asc) as continents,

    count(distinct community_id) filter (where community_id <> '') as communities_counted,

    sum(area_m2) as area_m2,
    st_union(geom) as geom

from public.communities

group by

    nation,

    country_id,
    country,

    region_id,
    region,
    region_type,
    
    district_id,
    district,
    district_type

order by this_uid;
