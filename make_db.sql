CREATE DATABASE IF NOT EXISTS inventorydb DEFAULT CHARACTER SET utf8mb4;

USE inventorydb;

CREATE TABLE IF NOT EXISTS product (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_name VARCHAR(50) UNIQUE NOT NULL,
  price INT NOT NULL,
  stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) UNIQUE NOT NULL,
  total INT NOT NULL,
  phone VARCHAR(50) UNIQUE NOT NULL,
  datetime DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  customer_id INT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES  customer(customer_id),
  product_id INT  NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  number INT NOT NULL
);

INSERT INTO product (
    product_name,
    price,
    stock
    )
VALUES 
    ('떡볶이', 3000, 30),
    ('치킨', 9000, 34),
    ('양파', 3200, 16),
    ('감자튀김', 3000, 547),
    ('치즈볼', 4000, 54),
    ('라면', 3000, 368),
    ('햄버거', 7500, 76),
    ('돈까스', 7000, 46);
    