
-- Uncomment to delete table
drop table if exists public.countries;

-- Create new table
create table if not exists public.countries as

select distinct

    row_number() over (order by min(this_uid)) as this_uid,
    nation,

    country_id,
    country,

    array_agg(distinct region_id order by region_id asc) filter (where region_id <> '') as region_ids,

    array_agg(distinct region order by region asc) filter (where region <> '') as regions,
    
    array_agg(distinct region_type order by region_type asc) filter (where region_type <> '') as region_types,
    
    count(distinct region_id) filter (where region_id <> '') as regions_counted,
    

    array_agg(distinct continent order by continent asc) as continents,

    count(distinct continent) as continents_counted,

    sum(area_m2) as area_m2,
    st_union(geom) as geom

from public.regions

cross join lateral unnest(continents) as continent

group by

    nation,

    country_id,
    country,

    region_id,
    region,
    region_type

order by this_uid;
