
-- Uncomment to delete table
drop table if exists public.areas;

-- Create new table
create table if not exists public.areas as

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
    
    area_id,
    area,
    area_type,
    
    array_agg(distinct territory_id order by territory_id asc) filter (where territory_id <> '') as territory_ids,

    array_agg(distinct territory order by territory asc) filter (where territory <> '') as territories,

    array_agg(distinct territory_type order by territory_type asc) filter (where territory_type <> '') as territory_types,
    
    count(distinct territory_id) filter (where territory_id <> '') as territories_counted,
    
    continent,

    st_area(st_unaryunion(st_collect(geom))::geography) as area_m2,
    st_union(geom) as geom

from public.territories

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
    
    area_id,
    area,
    area_type,

    continent

order by this_uid;
