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