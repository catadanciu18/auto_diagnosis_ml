import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from config import TRAIN_DATA_PATH, TARGET_COLUMN, MODEL_PATH, LABEL_ENCODER_PATH


def main():
    if not os.path.exists(TRAIN_DATA_PATH):
        print("Nu există datasetul.")
        print("Rulează mai întâi: python scripts/generate_dataset.py")
        return

    df = pd.read_csv(TRAIN_DATA_PATH)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    categorical_columns = ["brand", "model", "engine_type", "engine_code"]
    numeric_columns = [col for col in X.columns if col not in categorical_columns]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
            ("num", "passthrough", numeric_columns),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        random_state=42,
        class_weight="balanced"
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Weighted F1:", f1_score(y_test, y_pred, average="weighted"))
    print()
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))

    os.makedirs("models", exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)

    print()
    print("Model salvat în:", MODEL_PATH)
    print("Label encoder salvat în:", LABEL_ENCODER_PATH)


if __name__ == "__main__":
    main()