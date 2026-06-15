
-- Uncomment to delete table
drop table if exists public.communities;

-- Create new table
create table if not exists public.communities as

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
    
    community_id,
    community,
    community_type,
    
    array_agg(distinct area_id order by area_id asc) filter (where area_id <> '') as area_ids,
    
    array_agg(distinct area order by area asc) filter (where area <> '') as areas,
    
    array_agg(distinct area_type order by area_type asc) filter (where area_type <> '') as area_types,
    
    count(distinct area_id) filter (where area_id <> '') as areas_counted,
    
    continent,

    st_area(st_unaryunion(st_collect(geom))::geography) as area_m2,
    st_union(geom) as geom

from public.areas

group by

    nation,

    country_id,
    country,

    region_id,
    region,
    region_type,
    
    district_id,
    district,
    district_type,
    
    community_id,
    community,
    community_type,

    continent

order by this_uid;
