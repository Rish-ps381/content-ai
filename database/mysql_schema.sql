-- MySQL schema for the retail SQL data agent.
-- Based on the actual CSV files in data/.

CREATE DATABASE IF NOT EXISTS `agentic_ai`;
USE `agentic_ai`;

CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` VARCHAR(16) NOT NULL,
  `customer_segment` VARCHAR(32) NOT NULL,
  `signup_date` DATE NOT NULL,
  `preferred_channel` VARCHAR(32) NOT NULL,
  `city` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `products` (
  `product_id` VARCHAR(16) NOT NULL,
  `product_name` VARCHAR(128) NOT NULL,
  `category` VARCHAR(64) NOT NULL,
  `sub_category` VARCHAR(64) NOT NULL,
  `base_price` INT NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `stores` (
  `store_id` VARCHAR(16) NOT NULL,
  `store_name` VARCHAR(128) NOT NULL,
  `region` VARCHAR(32) NOT NULL,
  `city` VARCHAR(64) NOT NULL,
  `store_type` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`store_id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `sales_transactions` (
  `order_id` VARCHAR(16) NOT NULL,
  `order_date` DATE NOT NULL,
  `store_id` VARCHAR(16) NOT NULL,
  `product_id` VARCHAR(16) NOT NULL,
  `customer_id` VARCHAR(16) NOT NULL,
  `sales_channel` VARCHAR(32) NOT NULL,
  `units_sold` INT NOT NULL,
  `unit_price` DECIMAL(10,2) NOT NULL,
  `discount_pct` INT NOT NULL,
  `payment_status` VARCHAR(32) NOT NULL,
  `delivery_status` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `idx_sales_store` (`store_id`),
  KEY `idx_sales_product` (`product_id`),
  KEY `idx_sales_customer` (`customer_id`),
  CONSTRAINT `fk_sales_store` FOREIGN KEY (`store_id`) REFERENCES `stores`(`store_id`),
  CONSTRAINT `fk_sales_product` FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`),
  CONSTRAINT `fk_sales_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers`(`customer_id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `returns` (
  `return_id` VARCHAR(16) NOT NULL,
  `order_id` VARCHAR(16) NOT NULL,
  `return_date` DATE NOT NULL,
  `return_reason` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`return_id`),
  KEY `idx_returns_order` (`order_id`),
  CONSTRAINT `fk_returns_order` FOREIGN KEY (`order_id`) REFERENCES `sales_transactions`(`order_id`)
) ENGINE=InnoDB;
