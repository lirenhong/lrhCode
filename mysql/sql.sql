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

sql执行顺序:

from, where, select, group by, having, order by, limit

外键和关联主键数据类型一定要保持一致

select fieldlist from table1 [inner|left|right|all] join table2 on table1.column=table2.column

