create table transactions (id int not null auto_increment, description varchar(150), user_id int not null,category_id int, date date, value decimal(12,2) not null, primary key(id));
create table users (name varchar(100), email varchar(100), password varchar(150), id int auto_increment not null, primary key(id));
create table categories (id int not null auto_increment, category varchar(100) not null, user_id int not null, primary key(id));
create table accounts (id int not null auto_increment, name varchar(150), user_id int not null, type varchar(100), primary key(id));