import pandas as pd
from pathlib import Path


# =========================
# 1. Project Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

PROCESSED_DIR.mkdir(exist_ok=True)


# =========================
# 2. Read Raw Data
# =========================

customers = pd.read_csv(RAW_DIR / "customers.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")
returns = pd.read_csv(RAW_DIR / "returns.csv")
calendar = pd.read_csv(RAW_DIR / "calendar.csv")


# =========================
# 3. Convert Date Columns
# =========================

customers["signup_date"] = pd.to_datetime(customers["signup_date"])

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["delivery_date"] = pd.to_datetime(orders["delivery_date"])

returns["return_date"] = pd.to_datetime(returns["return_date"])

calendar["date"] = pd.to_datetime(calendar["date"])


# =========================
# 4. Basic Data Cleaning
# =========================

# Remove duplicate records
customers = customers.drop_duplicates()
products = products.drop_duplicates()
orders = orders.drop_duplicates()
returns = returns.drop_duplicates()

# Remove orders with missing important IDs
orders = orders.dropna(subset=["order_id", "customer_id", "product_id"])


# =========================
# 5. Create Order-Level Metrics
# =========================

orders = orders.merge(
    products[["product_id", "unit_price", "cost_price"]],
    on="product_id",
    how="left"
)

# Gross sales before discount
orders["gross_sales"] = orders["quantity"] * orders["unit_price"]

# Discount amount
orders["discount_amount"] = (
    orders["gross_sales"] * orders["discount"]
)

# Revenue after discount
orders["revenue"] = (
    orders["gross_sales"] - orders["discount_amount"]
)

# Product cost
orders["cost"] = (
    orders["quantity"] * orders["cost_price"]
)

# Profit
orders["profit"] = (
    orders["revenue"] - orders["cost"]
)


# =========================
# 6. Save Processed Data
# =========================

customers.to_csv(
    PROCESSED_DIR / "customers_clean.csv",
    index=False
)

products.to_csv(
    PROCESSED_DIR / "products_clean.csv",
    index=False
)

orders.to_csv(
    PROCESSED_DIR / "orders_clean.csv",
    index=False
)

returns.to_csv(
    PROCESSED_DIR / "returns_clean.csv",
    index=False
)

calendar.to_csv(
    PROCESSED_DIR / "calendar_clean.csv",
    index=False
)


# =========================
# 7. Pipeline Summary
# =========================

print("ETL Pipeline Completed Successfully!")
print("------------------------------------")
print("Customers:", len(customers))
print("Products:", len(products))
print("Orders:", len(orders))
print("Returns:", len(returns))

print("\nProcessed files saved in:", PROCESSED_DIR)