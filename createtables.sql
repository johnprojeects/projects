create table employee(
    employee_id number primary key,
    f_name varchar2(20) not null,
    l_name varchar2(20) not null,
    emp_role varchar2(20) check (emp_role in ('salesman', 'manager', 'supervisor')),
    works_for number references employee(employee_id),
    street_address varchar2(30),
    city varchar2(20),
    postal_code varchar2(10),
    province varchar(20)
);

create table customer(
    customer_id number primary key,
    f_name varchar2(20) not null,
    l_name varchar2(20) not null,
    email varchar2(30),
    phone number not null,
    street_address varchar2(20),
    city varchar2(20),
    postal_code varchar2(10),
    province varchar(20),
    loyalty_lvl number check (loyalty_lvl between 1 and 5)
);

CREATE TABLE rentals(
    rental_id number primary key,
    customer_id number references customer(customer_id),
    employee_id number references employee(employee_id),
    status varchar2(10) check (status in ('active', 'closed', 'cancelled')),
    cost decimal(30, 2),
    gross_profit decimal(30, 2),
    rental_date date not null,
    return_date date
);

create table equipment(
      equipment_id integer primary key,
      title varchar2(32) not null,
      equip_description varchar2(32),
      equip_type varchar2(32),
      model_num varchar2(32),
      qty_stocked smallint default 0,
      qty_available smallint
);

create table price_matrix(
    equipment_id number references equipment(equipment_id),
    sell_price1 number default 0,
    sell_price2 number default 0,
    sell_price3 number default 0,
    sell_price4 number default 0,
    sell_price5 number default 0,
    primary key(equipment_id)
);

create table rental_eqip_relate(
    rental_id number references rentals(rental_id),
    equipment_id number references equipment(equipment_id),
    qty_rented smallint default 1,
    primary key(rental_id, equipment_id)
);