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
drop table USER cascade;
drop table PERSON cascade;
drop table LIVES_IN cascade;
drop table RESPONSIBILITY cascade;
drop table chore_cattegory cascade;


create table PERSON
(
    user_id                         SERIAL primary key,
    user_name                       varchar(100) not null,
    user_email                      varchar(100) not null,
    admin                           bool,
    user_password                   varchar(1000) not null
);

create table HOME
(
    home_id                         SERIAL primary key,
    home_name                       varchar(100) not null
);

create table CHORE
(
    chore_id                        SERIAL primary key,
    chore_name                      varchar(100) not null,
    chore_description               varchar(500) not null 
);

create table RESPONSIBILITY
(
    user_id                         int,
    chore_id                        int,
    worth                           int,
    primary key(chore_id),
    foreign key(user_id)            references PERSON(user_id),
    foreign key(chore_id)           references CHORE(chore_id)
);
    


create table LIVES_IN
(
    user_id                         int,
    home_id                         int,
    primary key(user_id),
    FOREIGN key(user_id)            REFERENCES PERSON(user_id),
    FOREIGN key(home_id)            REFERENCES HOME(home_id)
);

create table BANK_ACCOUNT
(
    user_id                         int not null,
    account_balance                 int not null,
    foreign key(user_id)            references PERSON(user_id)
);