
with scratch as (

    select distinct

        -- array_agg(distinct this_uid) as parent_uid_list,
        
        nation,
        
        country_id,
        country,

        region_id,
        region,
        region_type,
        
        district_id,
        district,
        district_type,

        -- community_id,
        -- community,
        -- community_type,
        
        -- area_id,
        -- area,
        -- area_type,
        
        -- territory_id,
        -- territory,
        -- territory_type,

        -- array_agg(distinct continent) as continents,
        count(distinct continent) as continents_counted

    -- from public.territories
    -- from public.areas
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

        -- community_id,
        -- community,
        -- community_type
        
        -- area_id,
        -- area,
        -- area_type,
        
        -- territory_id,
        -- territory,
        -- territory_type,

        -- continent

    order by

        nation asc,
        country asc,
        region asc,
        district asc
        -- community asc
        -- area asc,
        -- territory asc

)

select count(*)

from scratch

where continents_counted > 1;