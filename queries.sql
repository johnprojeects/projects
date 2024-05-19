SELECT f_name
FROM customer
WHERE loyalty_lvl >= 2;

SELECT email
FROM customer
WHERE province = 'Ontario';

SELECT f_name, l_name, 'is a: ', emp_role
FROM employee
WHERE emp_role = 'manager';

SELECT f_name, l_name, 'is a: ', emp_role
FROM employee
WHERE emp_role = 'salesman';

SELECT *
FROM equipment
WHERE qty_available > 0;

SELECT equipment_id
FROM price_matrix
WHERE sell_price2 <= 25;

SELECT *
FROM rental_eqip_relate
WHERE qty_rented = 1;

SELECT rental_id, 'was rented on: ', rental_date
FROM rentals
WHERE status = 'active';