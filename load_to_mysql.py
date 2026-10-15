import pandas as pd
import mysql.connector
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "processed"

# Batch size
BATCH_SIZE = 5000

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_analytics"
)

print("MySQL connected successfully!")

cursor = connection.cursor()


def load_in_batches(query, data, table_name):
    total = len(data)

    for start in range(0, total, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total)
        batch = data[start:end]

        cursor.executemany(query, batch)
        connection.commit()

        print(f"{table_name} loaded: {end}/{total}")


# --------------------------------------------------
# 1. Load Customers
# --------------------------------------------------

customers = pd.read_csv(
    PROCESSED_DIR / "customers_clean.csv"
)

customer_query = """
INSERT INTO customers
(customer_id, customer_name, gender, age, city, state, signup_date)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

customer_data = [
    tuple(row)
    for row in customers.itertuples(index=False, name=None)
]

load_in_batches(
    customer_query,
    customer_data,
    "Customers"
)


# --------------------------------------------------
# 2. Load Products
# --------------------------------------------------

products = pd.read_csv(
    PROCESSED_DIR / "products_clean.csv"
)

product_query = """
INSERT INTO products
(product_id, product_name, category, sub_category, unit_price, cost_price)
VALUES (%s, %s, %s, %s, %s, %s)
"""

product_data = [
    tuple(row)
    for row in products.itertuples(index=False, name=None)
]

load_in_batches(
    product_query,
    product_data,
    "Products"
)


# --------------------------------------------------
# 3. Load Orders
# --------------------------------------------------

orders = pd.read_csv(
    PROCESSED_DIR / "orders_clean.csv"
)

order_query = """
INSERT INTO orders
(order_id, customer_id, product_id, order_date, quantity,
discount, payment_method, order_status, delivery_date,
delivered_on_time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

order_columns = [
    "order_id",
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount",
    "payment_method",
    "order_status",
    "delivery_date",
    "delivered_on_time"
]

order_data = [
    tuple(row)
    for row in orders[order_columns].itertuples(
        index=False,
        name=None
    )
]

load_in_batches(
    order_query,
    order_data,
    "Orders"
)


# --------------------------------------------------
# 4. Load Returns
# --------------------------------------------------

returns = pd.read_csv(
    PROCESSED_DIR / "returns_clean.csv"
)

return_query = """
INSERT INTO returns
(return_id, order_id, return_date, return_reason)
VALUES (%s, %s, %s, %s)
"""

return_data = [
    tuple(row)
    for row in returns.itertuples(index=False, name=None)
]

load_in_batches(
    return_query,
    return_data,
    "Returns"
)


# --------------------------------------------------
# 5. Load Calendar
# --------------------------------------------------

calendar = pd.read_csv(
    PROCESSED_DIR / "calendar_clean.csv"
)

calendar_query = """
INSERT INTO calendar
(date)
VALUES (%s)
"""

calendar_data = [
    (row,)
    for row in calendar["date"]
]

load_in_batches(
    calendar_query,
    calendar_data,
    "Calendar"
)

# --------------------------------------------------
# Close connection
# --------------------------------------------------

cursor.close()
connection.close()

print("\nAll data loaded successfully into MySQL!")