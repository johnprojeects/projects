INSERT INTO CUSTOMER (customer_id, F_NAME, L_NAME, EMAIL, PHONE, STREET_ADDRESS, CITY, POSTAL_CODE, PROVINCE, LOYALTY_LVL) 
VALUES (1, 'Eric', 'Muzzo', 'eric.muzzo@torontomu.ca', 6471234567, 'Squire Drive', 'Richmond Hill', 'L4S1C7', 'Ontario', 1);

INSERT INTO CUSTOMER (customer_id, F_NAME, L_NAME, EMAIL, PHONE, STREET_ADDRESS, CITY, POSTAL_CODE, PROVINCE, LOYALTY_LVL) 
VALUES (2, 'John', 'Li', 'john.li@torontomu.ca', 6479876543, 'Dundas Street', 'Toronto', 'M5G2C2', 'Ontario', 2);

INSERT INTO CUSTOMER (customer_id, F_NAME, L_NAME, EMAIL, PHONE, STREET_ADDRESS, CITY, POSTAL_CODE, PROVINCE, LOYALTY_LVL) 
VALUES (3, 'Vigas', 'Balachandran', 'vigas.b@torontomu.ca', 6473336576, 'Haida Drive', 'Aurora', 'L4G3C7', 'Ontario', 3);

INSERT INTO EMPLOYEE (employee_id, f_name, l_name, emp_role, street_address, city, postal_code, province)
VALUES (1, 'Elon', 'Musk', 'supervisor', 'Imaginary Drive', 'Markham', 'L4S1C8', 'Ontario');

INSERT INTO EMPLOYEE 
VALUES (2, 'Joe', 'Rogan', 'manager', '1', 'Belville Court', 'Scarborough', 'G2B8R4', 'Ontario');

INSERT INTO EMPLOYEE 
VALUES (3, 'Jeff', 'Bezos', 'salesman', '2', 'Flemmings Road', 'Bolton', 'A1B2C3', 'Ontario');

INSERT INTO equipment
VALUES (33190, 'Cannon Rebel T5I DSLR Camera', NULL, 'Cameras', 't5i', 5, 1);

INSERT INTO equipment
VALUES (22467, 'DSLR Adjustable Tripod', NULL, 'Camera Accessories', 'TP123', 8, 2);

INSERT INTO equipment
VALUES (46982, '18" Ring Light', NULL, 'Lighting', 'R987', 3, 2);

INSERT INTO price_matrix (equipment_id, sell_price1, sell_price2, sell_price3)
VALUES (33190, 35.00, 33.00, 30.00);

INSERT INTO price_matrix (equipment_id, sell_price1, sell_price2, sell_price3)
VALUES (22467, 20.00, 18.00, 15.00);

INSERT INTO price_matrix (equipment_id, sell_price1, sell_price2, sell_price3)
VALUES (46982, 27.00, 25.00, 22.00);

INSERT INTO rentals (rental_id, customer_id, employee_id, status, rental_date)
VALUES (1, 1, 3, 'active', '2023-09-25');

INSERT INTO rental_eqip_relate
VALUES (1, 33190, 1);

INSERT INTO rental_eqip_relate
VALUES (1, 22467, 2);

INSERT INTO rentals (rental_id, customer_id, employee_id, status, rental_date, return_date)
VALUES (2, 2, 3, 'closed', '2023-08-23', '2023-09-24');

INSERT INTO rental_eqip_relate
VALUES (2, 46982, 2);

INSERT INTO rentals (rental_id, customer_id, employee_id, status, rental_date)
VALUES (3, 3, 2, 'cancelled', '2022-01-14');

INSERT INTO rental_eqip_relate
VALUES (3, 46982, 1);

INSERT INTO rental_eqip_relate
VALUES (3, 22467, 1);