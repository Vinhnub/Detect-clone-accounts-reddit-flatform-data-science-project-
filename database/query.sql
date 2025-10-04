create table r_user (
	username varchar(30) primary key,
	link_karma int not null, 
	comment_karma int not null,
	created datetime not null,
	premium bit not null,
	verified_email bit not null
);

create table achiverment (
	achiverment_name varchar(50) primary key
)

create table user_achiverment (
	username varchar(30) not null references r_user(username),
	achiverment_name varchar(50) not null references achiverment(achiverment_name),
	constraint u_a primary key (username, achiverment_name)
)

create table post (
	id varchar(15) primary key,
	subreddit varchar(30) not null,
	title nvarchar(400) not null,
	content nvarchar(MAX),
	p_url varchar(1000) not null,
	score int not null,
	created datetime not null,
	username varchar(30) not null references r_user(username)
)

create table comment (
	id varchar(15) primary key,
	body nvarchar(MAX) not null,
	subreddit varchar(30) not null,
	score int not null,
	created datetime not null,
	username varchar(30) not null references r_user(username)
)

drop table comment
drop table post
drop table user_achiverment
drop table achiverment
drop table r_user

select *
from post
where score <= 0
order by score

