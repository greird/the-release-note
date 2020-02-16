create table if not exists dim_artist
(
    id         serial                  not null,
    name       varchar,
    nb_fans    integer,
    artist_id  integer                 not null
        constraint dim_artist_pk
            primary key,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);

create unique index dim_artist_id_uindex
    on dim_artist (id);

create unique index dim_artist_artist_id_uindex
    on dim_artist (artist_id);


