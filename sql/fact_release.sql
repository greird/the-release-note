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


