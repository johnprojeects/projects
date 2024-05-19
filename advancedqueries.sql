CREATE VIEW equip_available AS
SELECT title, equip_description, model_num, qty_available
FROM equipment
WHERE qty_available > 0;

CREATE VIEW INVOICE AS
SELECT R.RENTAL_ID, C.F_NAME, C.L_NAME, R.RENTAL_DATE, R.GROSS_PROFIT AS TOTAL,
E.F_NAME || ' ' || E.L_NAME AS EMPLOYEE 
FROM RENTALS R
JOIN CUSTOMER C ON R.CUSTOMER_ID = C.CUSTOMER_ID
JOIN EMPLOYEE E ON R.EMPLOYEE_ID = E.EMPLOYEE_ID;

CREATE VIEW possible_managers ("EMPLOYEE_ID", "FULL_NAME") AS 
 (SELECT EMPLOYEE_ID, F_NAME || ' ' || L_NAME
 FROM employee
 WHERE emp_role = 'salesman')
WITH READ ONLY;

SELECT c.Customer_ID, c.F_name, 'had a rental started by: ', e.F_name
FROM customer c, rentals r, employee e
WHERE Status = 'closed'
      AND e.F_name = 'Jeff'
      AND c.Customer_ID = r.Customer_ID
      AND e.Employee_ID = r.Employee_ID
ORDER BY c.Customer_ID DESC;

SELECT c.F_name, c.L_name, 'rented multiple: ', e.title
FROM customer c, rentals r, rental_eqip_relate o, equipment e
WHERE qty_rented > 1
      AND c.Customer_ID = r.Customer_ID
      AND o.Rental_ID = r.Rental_ID
      AND o.Equipment_ID = e.Equipment_ID
ORDER BY title ASC;

SELECT e.F_name, 'is available to help ', c.F_name, 'close a rental'
FROM customer c, rentals r, employee e
WHERE Status = 'active'
      AND r.Customer_ID = c.Customer_ID
      AND c.City = e.City
ORDER BY e.F_name;