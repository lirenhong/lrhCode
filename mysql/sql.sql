CREATE TABLE employee(
	id TINYINT PRIMARY KEY auto_increment,
	name varchar(25),
	gender boolean,
	age INT DEFAULT 19,
	department VARCHAR(20),
	salary DOUBLE(7, 2)
);

alter table employee add is_marrid TINYINT(1);

alter table employee add entry_date date not null;

alter table employee drop is_marrid;

alter table employee modify age smallint not null default 18 after id;

alter table employee change department depart varchar(20) after salary;

rename table employee to emp;

drop table A;

select distinct name from emp

select name + 10 (as) 姓名 from emp

select name from emp where name like 'li%'('li_')