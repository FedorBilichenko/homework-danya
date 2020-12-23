CREATE DATABASE technics;

CREATE TABLE IF NOT EXISTS consigments(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    employer VARCHAR(50) NOT NULL,
    count INT NOT NULL,
    time DATE NOT NULL
);

INSERT INTO consigments (name, employer, count, time) VALUES('Партия1', 'Поставщик1', 2, '2020-03-14');
INSERT INTO consigments (name, employer, count, time) VALUES('Партия2', 'Поставщик1', 2, '2019-11-25');
INSERT INTO consigments (name, employer, count, time) VALUES('Партия3', 'Поставщик2', 1, '2017-02-12');
INSERT INTO consigments (name, employer, count, time) VALUES('Партия4', 'Поставщик3', 1, '2018-01-01');
INSERT INTO consigments (name, employer, count, time) VALUES('Партия5', 'Поставщик4', 1, '2017-05-20');

CREATE TABLE IF NOT EXISTS products(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    unique_number VARCHAR(50) NOT NULL,
    life_time DATE NOT NULL,
    warranty_period DATE NOT NULL,
    consigment_id BIGINT NOT NULL REFERENCES consigments(id)
);

INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Компьюетер1', 'unique_number_1', '2024-02-12', '2022-03-14', 1);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Принтер1', 'unique_number_2', '2023-02-09', '2021-03-14', 1);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Сканер1', 'unique_number_3', '2025-03-14', '2023-03-14', 1);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Компьюетер2', 'unique_number_4', '2023-09-07', '2021-03-14', 2);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Компьюетер3', 'unique_number_5', '2020-03-25', '2020-01-01', 2);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Ноутбук1', 'unique_number_6', '2027-03-14', '2019-02-14', 3);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Ноутбук2', 'unique_number_7', '2024-02-14', '2019-01-14', 4);
INSERT INTO products (name, unique_number, life_time, warranty_period, consigment_id) VALUES('Ноутбук3', 'unique_number_8', '2023-03-15', '2020-03-14', 5);

CREATE TABLE IF NOT EXISTS employees(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    fio VARCHAR(100) NOT NULL,
    department VARCHAR(200) NOT NULL,
    age INT NOT NULL,
    product_id BIGINT NOT NULL REFERENCES products(id)
);

INSERT INTO employees(fio, age, department, product_id) VALUES('Игнатов Игнат Валерьевич', 16, 'Дизайн',1);
INSERT INTO employees(fio, age, department, product_id) VALUES('Абатов Иван Валерьевич', 25, 'Дизайн', 2);
INSERT INTO employees(fio, age, department, product_id) VALUES('Жмышенко Стас Альбертович', 60, 'Дизайн', 3);
INSERT INTO employees(fio, age, department, product_id) VALUES('Попов Даниил Павлович', 30, 'Программирование', 4);
INSERT INTO employees(fio, age, department, product_id) VALUES('Киричев Федор Александрович', 15, 'Программирование', 5);
INSERT INTO employees(fio, age, department, product_id) VALUES('Андреев Сергей Сергееви', 10, 'Программирование', 6);
INSERT INTO employees(fio, age, department, product_id) VALUES('Федоров Лаврентий Полиграфович', 14,'Продажи', 7);
INSERT INTO employees(fio, age, department, product_id) VALUES('Павлов Анатолий Женатович', 75, 'Продажи', 8);

SELECT
            employees.fio as employee_name,
            employees.department as employee_department,
            products.name as product_name,
            products.life_time as product_life_time,
            products.warranty_period as product_warranty_period,
            consigments.name as consigment_name,
            consigments.employer as consigment_employer,
            consigments.time as consigment_time
            FROM employees
            JOIN products
            ON employees.product_id = products.id
            JOIN consigments
            ON products.consigment_id = consigments.id
            WHERE employees.department = 'Дизайн' AND products.life_time::date > '2020-03-10' AND consigments.name = 'Партия № 1';