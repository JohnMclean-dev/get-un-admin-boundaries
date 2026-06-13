
-- Uncomment to delete table
drop table if exists public.regions;

-- Create new table
create table if not exists public.regions as

select distinct

    row_number() over (order by min(this_uid)) as this_uid,
    nation,

    country_id,
    country,

    region_id,
    region,
    region_type,
    
    array_agg(distinct district_id order by district_id asc) filter (where district_id <> '') as district_ids,

    array_agg(distinct district order by district asc) filter (where district <> '') as districts,
    
    array_agg(distinct district_type order by district_type asc) filter (where district_type <> '') as district_types,
    
    count(distinct district_id) filter (where district_id <> '') as districts_counted,
    
    
    array_agg(distinct continent order by continent asc) as continents,
    
    count(distinct continent) as continents_counted,

    sum(area_m2) as area_m2,
    st_union(geom) as geom

from public.districts

cross join lateral unnest(continents) as continent

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
