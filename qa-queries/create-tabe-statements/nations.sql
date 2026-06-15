
-- Uncomment to delete table
drop table if exists public.nations;

-- Create new table
create table if not exists public.nations as

select distinct

    row_number() over (order by min(this_uid)) as this_uid,
    nation,

    array_agg(distinct country_id order by country_id asc) filter (where country_id <> '') as country_ids,
    
    array_agg(distinct country order by country asc) filter (where country <> '') as countries,

    count(distinct country_id) filter (where country_id <> '') as countries_counted,


    array_agg(distinct continent order by continent asc) as continents,

    count(distinct continent) as continents_counted,

    st_area(st_unaryunion(st_collect(geom))::geography) as area_m2,
    st_union(geom) as geom

from public.countries

cross join lateral unnest(continents) as continent

group by nation

order by this_uid;
