import pandas as pd


def build_customer_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Convert purchase-level data into customer-level
    features for ML models.
    """

    if df.empty:
        return pd.DataFrame()

    df = df.copy()

    # Make sure purchase_date is a datetime
    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        errors="coerce"
    )

    # Remove rows where purchase date is invalid
    df = df.dropna(
        subset=["purchase_date"]
    )

    if df.empty:
        return pd.DataFrame()

    # --------------------------------------------------
    # Purchase frequency
    # --------------------------------------------------

    purchase_frequency = (
        df.groupby("customer_id")
        .size()
        .rename("purchase_frequency")
    )

    # --------------------------------------------------
    # Total amount spent
    # --------------------------------------------------

    total_spend = (
        df.groupby("customer_id")["total_amount"]
        .sum()
        .rename("total_spend")
    )

    # --------------------------------------------------
    # Average order value
    # --------------------------------------------------

    average_order_value = (
        df.groupby("customer_id")["total_amount"]
        .mean()
        .rename("average_order_value")
    )

    # --------------------------------------------------
    # Total quantity purchased
    # --------------------------------------------------

    total_quantity = (
        df.groupby("customer_id")["quantity"]
        .sum()
        .rename("total_quantity")
    )

    # --------------------------------------------------
    # Number of unique product categories
    # --------------------------------------------------

    category_count = (
        df.groupby("customer_id")["category"]
        .nunique()
        .rename("category_count")
    )

    # --------------------------------------------------
    # Number of unique products
    # --------------------------------------------------

    unique_product_count = (
        df.groupby("customer_id")["product_name"]
        .nunique()
        .rename("unique_product_count")
    )

    # --------------------------------------------------
    # Most recent purchase
    # --------------------------------------------------

    last_purchase = (
        df.groupby("customer_id")["purchase_date"]
        .max()
        .rename("last_purchase_date")
    )

    # --------------------------------------------------
    # Customer recency
    # --------------------------------------------------

    reference_date = df["purchase_date"].max()

    recency = (
        reference_date - last_purchase
    ).dt.days.rename("recency_days")

    # --------------------------------------------------
    # Customer demographic information
    # --------------------------------------------------

    demographic_columns = [
        "age",
        "gender",
        "city",
        "state",
        "country",
    ]

    available_demographics = [
        column
        for column in demographic_columns
        if column in df.columns
    ]

    customer_info = (
        df.sort_values(
            ["customer_id", "purchase_date"]
        )
        .groupby("customer_id")
        [available_demographics]
        .first()
    )

    # --------------------------------------------------
    # Combine all features
    # --------------------------------------------------

    features = pd.concat(
        [
            purchase_frequency,
            total_spend,
            average_order_value,
            total_quantity,
            category_count,
            unique_product_count,
            recency,
            customer_info,
        ],
        axis=1
    )

    features = features.reset_index()

    return features