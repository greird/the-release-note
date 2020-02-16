create table if not exists dim_user
(
    id         serial                  not null,
    first_name varchar,
    last_name  varchar,
    email      varchar,
    frequency  varchar,
    last_check timestamp default now() not null,
    user_id    integer                 not null
        constraint dim_user_pk
            primary key
);

create unique index dim_user_id_uindex
    on dim_user (id);

create unique index dim_user_user_id_uindex
    on dim_user (user_id);


