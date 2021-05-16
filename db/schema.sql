-- drop table if exists user;

create table if not exists user(
    user_id integer primary key autoincrement,
    username string not null,
    score string not null
);