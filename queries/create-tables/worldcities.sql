
DROP TABLE IF EXISTS public.worldcities;

CREATE TABLE IF NOT EXISTS public.worldcities (
    city text,
    city_ascii text,
    lat double precision,
    lng double precision,
    country text,
    iso2 text,
    iso3 text,
    admin_name text,
    capital text,
    population bigint,
    id bigint
);