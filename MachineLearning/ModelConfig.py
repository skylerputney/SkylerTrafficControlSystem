# File Path to Dataset
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from Config import BASE_DIR, DATA_DIR

MODEL_FILE_PATH = os.path.join(BASE_DIR, "Models")

# Model Initializations
MODELS = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(random_state=42),
    "XGBoost": XGBRegressor(random_state=42)
}

# Hyperparameter tuning configurations
PARAM_GRIDS = {
    "Random Forest": {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10]
    },
    "XGBoost": {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 6, 10],
        "learning_rate": [0.01, 0.1, 0.2],
        "subsample": [0.6, 0.8, 1.0]
    }
}

def get_latest_iteration_folder(folder_path=MODEL_FILE_PATH):
    """Returns the path of the most recently created model iteration folder in the given folder."""
    iteration_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    if not iteration_folders:
        return None

    latest_folder = max(iteration_folders, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    print(f"ModelConfig: Returning model folder: {latest_folder}")
    return os.path.join(folder_path, latest_folder)

def get_latest_dataset(folder_path=DATA_DIR):
    """Returns the path of the most recently created CSV file in the given folder."""
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not csv_files:
        return None

    latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    return os.path.join(folder_path, latest_csv)