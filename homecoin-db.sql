drop table HOME cascade;
drop table CHORE cascade;
drop table PERSON cascade;
drop table LIVES_IN cascade;
drop table RESPONSIBILITY cascade;
drop table AVATAR cascade;
drop table CATEGORY cascade;


create table PERSON
(
    user_id                         SERIAL primary key not null,
    user_name                       varchar(100) not null,
    user_email                      varchar(100) not null,
    admin                           bool not null,
    user_password                   varchar(1000) not null,
    user_avatar                     varchar(1000) not null
);

create table HOME
(
    home_id                         SERIAL primary key not null,
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
    user_id                         int not null,
    chore_id                        int not null,
    chore_worth                     int not null,
    deadline                        date not null,
    completed                       date,
    category                        varchar(500) not null,
    primary key(chore_id),
    foreign key(user_id)            references PERSON(user_id),
    foreign key(chore_id)           references CHORE(chore_id)
);
    


create table LIVES_IN
(
    user_id                         int not null,
    home_id                         int not null,
    primary key(user_id),
    FOREIGN key(user_id)            REFERENCES PERSON(user_id),
    FOREIGN key(home_id)            REFERENCES HOME(home_id)
);


create table AVATAR
(
    avatar_id                       SERIAL primary key,
    avatar_name                     varchar(500) not null,
    avatar_path                     varchar(500) not null
);

create table CATEGORY
(
    category_id                     SERIAL primary key,
    category_name                   varchar(500) not null,
    category_path                   varchar(500) not null                  
);


insert into AVATAR (avatar_name, avatar_path) VALUES(
    'Ninja', '/static/images/avatars/ninja.png'),
    ('Nurse','/static/images/avatars/nurse.png'),
    ('Angel','/static/images/avatars/angel.png'),
    ('Blueman','/static/images/avatars/blueman.png'),
    ('Bluewoman','/static/images/avatars/bluewoman.png'),
    ('Warrior','/static/images/avatars/warrior.png'),
    ('Viking','/static/images/avatars/viking.png'),
    ('Cyborg','/static/images/avatars/cyborg.png'),
    ('Devil','/static/images/avatars/devil.png'),
    ('Penguin','/static/images/avatars/penguin.png'),
    ('Police','/static/images/avatars/police.png'),
    ('Princess','/static/images/avatars/princess.png');


insert into CATEGORY (category_name, category_path) VALUES(
    'Damma', '/static/images/chores/dust.png'),
    ('Dammsug','/static/images/chores/vaccum.png'),
    ('Diska','/static/images/chores/dishes.png'),
    ('Hang tvatt','/static/images/chores/hanglaundry.png'),
    ('Ta ut sopor','/static/images/chores/trash.png'),
    ('Tvatta','/static/images/chores/laundry.png'),
    ('Skura','/static/images/chores/scrub.png'),
    ('Laga mat','/static/images/chores/cookfood.png'),
    ('Badda sangen','/static/images/chores/makebed.png'),
    ('Tvatta bilen','/static/images/chores/washcar.png'),
    ('Handla mat','/static/images/chores/grocery.png'),
    ('Annat','/static/images/chores/other.png');