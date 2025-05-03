import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from Config import BASE_DIR

# Max number of SUMO Simulation steps for Reinforcement Learning
RL_MAX_STEPS = 3000

# File Path to Supervised Models
SUPERVISED_MODEL_FILE_PATH = os.path.join(BASE_DIR, "Models", "Supervised")
# File Path to Reinforcement Models
REINFORCEMENT_MODEL_FILE_PATH = os.path.join(BASE_DIR, "Models", "Reinforcement")

# Name of model to run AITLController
AI_MODEL = "XGBoost"

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
