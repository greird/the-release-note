create table if not exists dim_album
(
    album_id     integer                 not null
        constraint dim_album_pk
            primary key,
    artist_id    integer,
    title        varchar,
    release_date timestamp,
    inserted_at  timestamp default now() not null,
    updated_at   timestamp default now() not null,
    nb_fans      integer,
    genre_id     integer,
    type         varchar
);

create unique index dim_album_album_id_uindex
    on dim_album (album_id);

create table if not exists dim_artist
(
    artist_id  integer                 not null
        constraint dim_artist_pk
            primary key,
    name       varchar,
    nb_fans    integer,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);

create unique index dim_artist_artist_id_uindex
    on dim_artist (artist_id);

create table if not exists dim_user
(
    user_id    integer                 not null
        constraint dim_user_pk
            primary key,
    first_name varchar,
    last_name  varchar,
    email      varchar,
    frequency  varchar,
    last_check timestamp default now() not null
);

create unique index dim_user_user_id_uindex
    on dim_user (user_id);

create table if not exists fact_releases
(
    id         serial    not null
        constraint fact_releases_pk
            primary key,
    user_id    integer,
    artist_id  integer,
    album_id   integer,
    created_at timestamp not null
);

create unique index fact_releases_id_uindex
    on fact_releases (id);