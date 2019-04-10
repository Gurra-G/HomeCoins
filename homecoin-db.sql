drop table TO_DO cascade;
drop table USERS cascade;
drop table USER_ROLE cascade;
drop table ROLES cascade;
drop table HOME cascade;
drop table CHORE cascade;
drop table CHORE_KEEPER cascade;
drop table COMPLETED_CHORE cascade;
drop table BANK cascade;
drop table BANK_ACCOUNT cascade;
drop table LIVING_IN cascade;

create table USERS
(
    user_id             SERIAL primary key,
    user_role           int not null,
    user_name           varchar(100) not null,
    user_email          varchar(100) not null,
    user_firstname      varchar(100) not null,
    user_lastname       varchar(100) not null,
    user_social_secnum  varchar(100) not null,
    user_password       varchar(100) not null,
    user_adress         varchar(100) not null,
    user_home_name      varchar(100) not null
    
);

create table ROLES
(
    role_id             integer primary key not null,
    role_name           varchar(20) not null,
    role_description    varchar(20) not null
);

create table USER_ROLE
(
    user_id                 int,
    role_id                 integer not null,
    primary key(user_id, role_id),
    foreign key(user_id) references USERS(user_id),
    foreign key(role_id) references ROLES(role_id)
);

create table HOME
(
    home_id                 SERIAL primary key,
    home_name               varchar(100) not null,
    home_adress            varchar(100) not null
);

create table CHORE
(
    chore_id                 SERIAL primary key,
    chore_name               varchar(100) not null,
    chore_cattegory          varchar(100) not null,
    chore_value              int not null,
    chore_description        varchar(500),
    due_date                 TIMESTAMP                    
);

create table CHORE_KEEPER
(
    home_id                         int,
    chore_id                        int,
    primary key(home_id, chore_id),
    foreign key(home_id)            references HOME(home_id),
    foreign key(chore_id)           references CHORE(chore_id)
);

create table TO_DO
(
    user_id                         int,
    chore_id                        int,
    primary key(user_id, chore_id),
    foreign key(user_id)            references USERS(user_id),
    foreign key(chore_id)           references CHORE(chore_id)

);

create table LIVING_IN
(
    user_id                         int,
    home_id                         int,
    primary key(user_id, home_id),
    FOREIGN key(user_id)            REFERENCES USERS(user_id),
    FOREIGN key(home_id)            REFERENCES HOME(home_id)
);

create table COMPLETED_CHORE
(
    sale_id                 SERIAL primary key,
    user_id                 int not null,
    chore_id                int not null,
    chore_value             integer not null,
    completion_date         timestamp(0) DEFAULT current_timestamp not null,
    foreign key(user_id)    references USERS(user_id),
    foreign key(chore_id)   references CHORE(chore_id)
);

create table BANK_ACCOUNT
(
    account_id                  SERIAL primary key,
    user_id                     int not null,
    account_balance             int not null,
    foreign key(user_id)        references USERS(user_id)
);

    
insert into ROLES(role_id, role_name, role_description) values
    (1, 'admin', 'parent'),
    (2, 'user', 'child');
