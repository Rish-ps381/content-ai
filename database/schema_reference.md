# Schema Reference

This draft schema is based only on the actual CSV contents in `data/`.

## customers.csv
- Rows: 80
- Columns:
  - `customer_id` (string)
  - `customer_segment` (string)
  - `signup_date` (string, date-like)
  - `preferred_channel` (string)
  - `city` (string)
- Likely primary key: `customer_id`
- No missing values observed.

## products.csv
- Rows: 10
- Columns:
  - `product_id` (string)
  - `product_name` (string)
  - `category` (string)
  - `sub_category` (string)
  - `base_price` (integer)
- Likely primary key: `product_id`
- No missing values observed.

## stores.csv
- Rows: 15
- Columns:
  - `store_id` (string)
  - `store_name` (string)
  - `region` (string)
  - `city` (string)
  - `store_type` (string)
- Likely primary key: `store_id`
- No missing values observed.

## sales_transactions.csv
- Rows: 360
- Columns:
  - `order_id` (string)
  - `order_date` (string, date-like)
  - `store_id` (string)
  - `product_id` (string)
  - `customer_id` (string)
  - `sales_channel` (string)
  - `units_sold` (integer)
  - `unit_price` (float)
  - `discount_pct` (integer)
  - `payment_status` (string)
  - `delivery_status` (string)
- Likely primary key: `order_id`
- No missing values observed.
- Revenue should be derived as `units_sold * unit_price`.

## returns.csv
- Rows: 46
- Columns:
  - `return_id` (string)
  - `order_id` (string)
  - `return_date` (string, date-like)
  - `return_reason` (string)
- Likely primary key: `return_id`
- No missing values observed.

## Relationships
- `sales_transactions.customer_id` → `customers.customer_id`
- `sales_transactions.product_id` → `products.product_id`
- `sales_transactions.store_id` → `stores.store_id`
- `returns.order_id` → `sales_transactions.order_id`

## Notes
- `order_id` appears in both `sales_transactions.csv` and `returns.csv`; this supports a returns join.
- `unit_price` and `units_sold` are the sales/revenue fields in `sales_transactions.csv`.
- All CSV files contained zero missing values in this inspection.
