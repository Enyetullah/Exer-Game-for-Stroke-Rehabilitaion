import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_user_data(user_name, game_type, data_dir="data"):
    """
    Load all session CSVs for the given user and game type.
    """
    user_path = os.path.join(data_dir, user_name)
    session_files = [
        f for f in os.listdir(user_path)
        if f.startswith(f"session_{game_type}") and f.endswith(".csv")
    ]

    all_data = []
    for file in session_files:
        session_path = os.path.join(user_path, file)
        df = pd.read_csv(session_path)
        all_data.append(df)

    if not all_data:
        raise ValueError(f"No session data found for user: {user_name}, game type: {game_type}")

    combined_df = pd.concat(all_data, ignore_index=True)
    failures = combined_df[combined_df["success"] == 0]

    # Add weight to failures to encourage model to focus on them
    partial_failures = failures.sample(frac=0.5, replace=True, random_state=42)
    combined_df = pd.concat([combined_df, partial_failures], ignore_index=True)

    return combined_df

def preprocess_user_data(df, game_type):
    """
    Create features and targets.
    """
    df = df.copy()

    if game_type.startswith("vertical"):
        df["distance"] = abs(df["ball_y"] - df["cup_y"])
    else:
        df["distance"] = abs(df["ball_x"] - df["cup_x"])

    def bucket_zone_horizontal(x, width=800):
        if x < width / 3:
            return "left"
        elif x < 2 * width / 3:
            return "center"
        else:
            return "right"

    def bucket_zone_vertical(y, height=600):
        if y < height / 3:
            return "top"
        elif y < 2 * height / 3:
            return "middle"
        else:
            return "bottom"

    if game_type.startswith("vertical"):
        df["zone"] = df["ball_y"].apply(bucket_zone_vertical)
        expected_zone_cols = ["zone_top", "zone_middle", "zone_bottom"]
    else:
        df["zone"] = df["ball_x"].apply(bucket_zone_horizontal)
        expected_zone_cols = ["zone_left", "zone_center", "zone_right"]

    # One-hot encode
    df = pd.get_dummies(df, columns=["zone"])

    # Ensure all expected zone columns are present
    for col in expected_zone_cols:
        if col not in df:
            df[col] = 0

    feature_cols = ["cup_x", "distance", "difficulty"] + expected_zone_cols
    X = df[feature_cols]
    y = df[expected_zone_cols].idxmax(axis=1).str.replace("zone_", "")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, X.columns.tolist()

def train_and_save_model(user_name, game_type, data_dir="data"):
    """
    Train RandomForest model for a specific user and game type.
    """
    print(f"[INFO] Training model for user '{user_name}' and game type '{game_type}'")

    # Load and preprocess data
    df = load_user_data(user_name, game_type, data_dir)
    X_scaled, y, scaler, column_order = preprocess_user_data(df, game_type)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_scaled, y)

    # Save model, scaler, and columns
    user_path = os.path.join(data_dir, user_name)
    os.makedirs(user_path, exist_ok=True)

    model_filename = f"model_{game_type}.pkl"
    scaler_filename = f"scaler_{game_type}.pkl"
    columns_filename = f"columns_{game_type}.txt"

    joblib.dump(model, os.path.join(user_path, model_filename))
    joblib.dump(scaler, os.path.join(user_path, scaler_filename))
    with open(os.path.join(user_path, columns_filename), "w") as f:
        f.write("\n".join(column_order))

    print(f"[SUCCESS] Model, scaler, and columns saved for user '{user_name}', game type '{game_type}'")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train personalized model for a user and game type")
    parser.add_argument("--user", type=str, required=True, help="User name to train model for")
    parser.add_argument("--game-type", type=str, required=True, help="Game type (e.g. horizontal_random, vertical_random, diagonal_workout)")
    args = parser.parse_args()

    train_and_save_model(args.user, args.game_type)
