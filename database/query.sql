-- create table r_user (
-- 	username varchar(30) primary key,
-- 	link_karma int not null, 
-- 	comment_karma int not null,
-- 	created datetime not null,
-- 	premium bit not null,
-- 	verified_email bit not null
-- );

-- create table achiverment (
-- 	achiverment_name varchar(50) primary key
-- )

-- create table user_achiverment (
-- 	username varchar(30) not null references r_user(username),
-- 	achiverment_name varchar(50) not null references achiverment(achiverment_name),
-- 	constraint u_a primary key (username, achiverment_name)
-- )

-- create table post (
-- 	id varchar(15) primary key,
-- 	subreddit varchar(30) not null,
-- 	title nvarchar(400) not null,
-- 	content nvarchar(MAX),
-- 	p_url varchar(1000) not null,
-- 	score int not null,
-- 	created datetime not null,
-- 	username varchar(30) not null references r_user(username)
-- )

-- create table comment (
-- 	id varchar(15) primary key,
-- 	body nvarchar(MAX) not null,
-- 	subreddit varchar(30) not null,
-- 	score int not null,
-- 	created datetime not null,
-- 	username varchar(30) not null references r_user(username)
-- )

-- drop table comment
-- drop table post
-- drop table user_achiverment
-- drop table achiverment
-- drop table r_user

-- select username, count(username) as number_user
-- from r_user
-- where link_karma + comment_karma > 100
-- group by username


-- select * 
-- from r_user


CREATE TABLE r_user (
    username TEXT PRIMARY KEY,
    link_karma INTEGER NOT NULL,
    comment_karma INTEGER NOT NULL,
    created TEXT NOT NULL,         
    premium INTEGER NOT NULL,       
    verified_email INTEGER NOT NULL 
);

CREATE TABLE achievement (
    achievement_name TEXT PRIMARY KEY
);

CREATE TABLE user_achievement (
    username TEXT NOT NULL,
    achievement_name TEXT NOT NULL,
    PRIMARY KEY (username, achievement_name),
    FOREIGN KEY (username) REFERENCES r_user(username),
    FOREIGN KEY (achievement_name) REFERENCES achievement(achievement_name)
);

CREATE TABLE post (
    id TEXT PRIMARY KEY,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,                 
    p_url TEXT NOT NULL,
    score INTEGER NOT NULL,
    created TEXT NOT NULL,         
    username TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES r_user(username)
);

CREATE TABLE comment (
    id TEXT PRIMARY KEY,
    body TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    score INTEGER NOT NULL,
    created TEXT NOT NULL,
    username TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES r_user(username)
);
