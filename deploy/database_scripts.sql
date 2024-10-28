create table users
(
    user_id uuid default gen_random_uuid() not null
        primary key,
    name    varchar(255)                   not null,
    email   varchar(255)                   not null
);

alter table users
    owner to postgres;

create table hotels
(
    hotel_id   uuid default gen_random_uuid() not null
        primary key,
    hotel_name varchar(300),
    address    varchar(255)
);

alter table hotels
    owner to postgres;

create table reviews
(
    review_id uuid default gen_random_uuid() not null
        primary key,
    user_id   uuid
        references users,
    hotel_id  uuid
        references hotels,
    rating    integer,
    comment   text
);

alter table reviews
    owner to postgres;

