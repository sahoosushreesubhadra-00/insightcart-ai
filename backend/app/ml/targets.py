import pandas as pd


TARGET_COLUMN = "total_spend"


def build_spending_target(
    features: pd.DataFrame
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare customer data for spending prediction.

    Returns:
        X: Input features
        y: Target variable (total_spend)
    """

    if features.empty:
        raise ValueError(
            "Feature dataset is empty."
        )

    if TARGET_COLUMN not in features.columns:
        raise ValueError(
            f"Required target column "
            f"'{TARGET_COLUMN}' is missing."
        )

    df = features.copy()

    # Convert target to numeric
    df[TARGET_COLUMN] = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    # Remove invalid target values
    df = df.dropna(
        subset=[TARGET_COLUMN]
    )

    # Spending cannot be negative
    df = df[
        df[TARGET_COLUMN] >= 0
    ]

    if df.empty:
        raise ValueError(
            "No valid target values available."
        )

    # Target
    y = df[TARGET_COLUMN].copy()

    # Remove target from input features
    X = df.drop(
        columns=[TARGET_COLUMN]
    ).copy()

    # customer_id is an identifier, not a useful
    # predictive feature
    if "customer_id" in X.columns:
        X = X.drop(
            columns=["customer_id"]
        )

    return X, y