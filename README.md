# DRF Assessment Backend

Backend APIs for Customer, Store (Product & Order), and Transaction modules using Django REST Framework viewsets.

## Quickstart

1. Create venv and install deps
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
2. Migrate and run
   - `python manage.py migrate`
   - `python manage.py runserver`

Default DB is SQLite in `db.sqlite3`.

## Models

- Customer: `first_name`, `last_name`, `email (unique)`, `address`, `created_at`, `updated_at`.
- Product: `name`, `amount>=0`, `discount>=0`, `quantity>=0`, timestamps; validation prevents `discount>amount`.
- Order: `customer`, `product`, `total_amount`, `created_at`. Create requires `quantity`; computes `total_amount=(amount-discount)*quantity`; decrements product stock atomically and prevents insufficient stock.
- Transaction: one-to-one with `Order`, `trx_id (unique)`, `created_at`. Ensures one transaction per order.

## Endpoints

Base path: `/`

- Customers
  - `POST /customers/` create
  - `GET /customers/` list
  - `GET /customers/{id}/` retrieve
  - `PUT/PATCH /customers/{id}/` update
  - `DELETE /customers/{id}/` delete
  - Filtering: `?search=...` (name/email), `?email=...`

- Products
  - `POST /products/` create
  - `GET /products/` list
  - `GET /products/{id}/` retrieve
  - `PUT/PATCH /products/{id}/` update
  - `DELETE /products/{id}/` delete
  - Filtering: `?name=...&min_amount=...&max_amount=...&in_stock=true|false`

- Orders
  - `POST /orders/` create with body: `{"customer":<id>, "product":<id>, "quantity":<int>}`
  - `GET /orders/` list
  - `GET /orders/{id}/` retrieve
  - Filtering: `?customer=...&product=...&created_after=ISO&created_before=ISO`

- Transactions
  - `POST /transactions/` create `{"order":<id>, "trx_id":"..."}` (one per order enforced)
  - `GET /transactions/` list
  - `GET /transactions/{id}/` retrieve
  - Filtering: `?trx_id=...&order=...`

## Pagination, Search, Ordering

- PageNumber pagination: `?page=1` (size 10 by default).
- Search and filtering via `django-filter` and DRF built-ins.
- Ordering via `?ordering=created_at` (prefix with `-` for desc) on supported viewsets.

## Notes

- Unique constraints: `Customer.email`, `Transaction.trx_id`. One transaction per order (`OneToOne`).
- Business rules enforced in `OrderSerializer.create()`.
- Adjust `REST_FRAMEWORK` or database settings in `config/settings.py` as needed.

