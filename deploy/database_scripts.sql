create table users
(
    user_id uuid,
    name    varchar(255),
    email   varchar(255)
);

alter table users
    owner to postgres;

