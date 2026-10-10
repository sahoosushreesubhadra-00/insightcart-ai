import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def prepare_features(
    df: pd.DataFrame
):
    """
    Prepare customer features for machine learning.
    """

    if df.empty:
        return None, None

    df = df.copy()

    categorical_columns = [
        "gender",
        "city",
        "state",
        "country",
    ]

    numerical_columns = [
        "purchase_frequency",
        "total_spend",
        "average_order_value",
        "total_quantity",
        "category_count",
        "recency_days",
        "age",
    ]

    # Keep only columns that actually exist
    categorical_columns = [
        column
        for column in categorical_columns
        if column in df.columns
    ]

    numerical_columns = [
        column
        for column in numerical_columns
        if column in df.columns
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_columns,
            ),
            (
                "numerical",
                "passthrough",
                numerical_columns,
            ),
        ]
    )

    X = preprocessor.fit_transform(
        df[categorical_columns + numerical_columns]
    )

    return X, preprocessor