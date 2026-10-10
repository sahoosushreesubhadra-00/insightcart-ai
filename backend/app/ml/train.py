import os
import joblib

from sqlalchemy.orm import Session

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from app.ml.data_loader import load_purchase_data
from app.ml.features import build_customer_features
from app.ml.targets import build_spending_target


MODEL_DIR = "/app/models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "customer_spending_model.joblib"
)


def train_customer_spending_model(
    db: Session
):
    """
    Train a customer spending prediction model.

    total_spend is the target variable and is
    intentionally excluded from the input features
    to prevent target leakage.
    """

    # --------------------------------------------------
    # 1. Load purchase data
    # --------------------------------------------------

    df = load_purchase_data(db)

    if df.empty:
        raise ValueError(
            "No purchase data available for training."
        )

    print(
        f"Loaded {len(df)} purchase records."
    )

    # --------------------------------------------------
    # 2. Build customer-level features
    # --------------------------------------------------

    features = build_customer_features(df)

    if features.empty:
        raise ValueError(
            "Unable to build customer features."
        )

    print(
        f"Built features for "
        f"{len(features)} customers."
    )

    # --------------------------------------------------
    # 3. Build X and y
    # --------------------------------------------------

    X, y = build_spending_target(features)

    # IMPORTANT:
    # total_spend must NOT be included in X.
    #
    # build_spending_target() already removes it,
    # but we explicitly check here so future changes
    # cannot accidentally introduce target leakage.

    if "total_spend" in X.columns:
        X = X.drop(
            columns=["total_spend"]
        )

    # customer_id is an identifier, not a predictive
    # feature.
    if "customer_id" in X.columns:
        X = X.drop(
            columns=["customer_id"]
        )

    print(
        f"Training features: {X.shape}"
    )

    print(
        f"Target values: {y.shape}"
    )

    print(
        "\nFeatures used for training:"
    )

    for column in X.columns:
        print(f" - {column}")

    print(
        "\nTarget:"
    )

    print(" - total_spend")

    # --------------------------------------------------
    # 4. Identify categorical columns
    # --------------------------------------------------

    categorical_columns = [
        column
        for column in [
            "gender",
            "city",
            "state",
            "country",
        ]
        if column in X.columns
    ]

    numerical_columns = [
        column
        for column in X.columns
        if column not in categorical_columns
    ]

    # --------------------------------------------------
    # 5. Preprocessing
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 6. Create regression model
    # --------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )

    # --------------------------------------------------
    # 7. Create ML pipeline
    # --------------------------------------------------

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    # --------------------------------------------------
    # 8. Train / test split
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    print(
        f"\nTraining records: {len(X_train)}"
    )

    print(
        f"Testing records: {len(X_test)}"
    )

    # --------------------------------------------------
    # 9. Train model
    # --------------------------------------------------

    print(
        "\nTraining model..."
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    print(
        "Model training completed."
    )

    # --------------------------------------------------
    # 10. Make predictions
    # --------------------------------------------------

    predictions = pipeline.predict(
        X_test
    )

    # --------------------------------------------------
    # 11. Evaluate model
    # --------------------------------------------------

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions,
    )

    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }

    print(
        "\nModel Evaluation"
    )

    print(
        "------------------------"
    )

    print(
        f"MAE  : {mae:.2f}"
    )

    print(
        f"RMSE : {rmse:.2f}"
    )

    print(
        f"R²   : {r2:.4f}"
    )

    # --------------------------------------------------
    # 12. Save model
    # --------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True,
    )

    joblib.dump(
        pipeline,
        MODEL_PATH,
    )

    print(
        f"\nModel saved to: {MODEL_PATH}"
    )

    return pipeline, metrics