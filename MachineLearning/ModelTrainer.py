import os
import pandas as pd
from datetime import datetime
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from xgboost.testing.data import joblib
import joblib
from Config import DATA_DIR
from FileManager.FileManager import FileManager
from MachineLearning.ModelConfig import get_latest_dataset, MODEL_FILE_PATH, MODELS, PARAM_GRIDS


class ModelTrainer:
    """
    Trains and evaluates Machine Learning Models using latest simulation data
    """
    def __init__(self, iteration=1):
        self.iteration = iteration  # Iteration of consecutive training
        self.training_data_path = get_latest_dataset()
        self.data_manager = FileManager(DATA_DIR)
        self.model_manager = FileManager(MODEL_FILE_PATH)

    def get_features_and_targets(self):
        """
        Defines features (X) and target variables (Y) for model training,
        Split the data into training and testing sets,
        Scale Features
        :return: X_train_scaled, X_test_scaled, Y_train, Y_test
        """
        # Read in data
        data = self.data_manager.load_latest_csv()

        # Define features (X) and target variables (Y)
        X = data[['state', 'phase_duration', 'current_phase_time']]
        Y = data[['phase_duration']] # Testing w/o state

        # Split data into training and testing sets
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.fit_transform(X_test)

        return X_train_scaled, X_test_scaled, Y_train, Y_test

    def train_models(self, iteration=1):
        #Update iteration#
        self.iteration = iteration

        # Create model output directory
        output_dir = self.model_manager.create_sub_dir(f"iteration{self.iteration}_{datetime.now().strftime('%Y%m%d%H%M%S')}")

        # Get features and targets
        X_train, X_test, Y_train, Y_test = self.get_features_and_targets()

        # Loop through MODELS defined in ModelConfig and train them based on latest data
        for model_name, model in MODELS.items():
            print(f"ModelTrainer: Training {model_name}...")

            # Load most recent model iteration
            loaded_model = self.load_latest_model(model_name)
            model = loaded_model if loaded_model is not None else model

            # Hyperparameter tuning for models that need it
            if model_name in PARAM_GRIDS:
                grid_search = GridSearchCV(model, PARAM_GRIDS[model_name], cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
                grid_search.fit(X_train, Y_train.values.ravel())
                model = grid_search.best_estimator_
                print(f"ModelTrainer: Best parameters for {model_name}: {grid_search.best_params_}")
            else:
                model.fit(X_train, Y_train.values.ravel())

            # Save trained model
            model_path = os.path.join(output_dir, f"{model_name.replace(' ', '_')}.pkl")
            joblib.dump(model, model_path)
            print(f"ModelTrainer: {model_name} saved to {model_path}")

            # Test model
            # Predictions
            Y_pred = model.predict(X_test)
            # Evaluation
            mse = mean_squared_error(Y_test, Y_pred)
            r2 = r2_score(Y_test, Y_pred)
            print(f"ModelTrainer: {model_name} - MSE: {mse:.2f}, R² Score: {r2:.2f}")
            # Save metrics
            with open(os.path.join(output_dir, f"{model_name.replace(' ', '_')}_metrics.txt"),
                      "w") as f:
                f.write(f"MSE: {mse:.2f}\nR²: {r2:.2f}\n")

        print(f"ModelTrainer: Iteration {iteration} completed. Results saved to {output_dir}")


    def load_latest_model(self, model_name):
        """
        Load the latest trained model from the Models directory
        :param model_name: Name of model to load
        :return: model, None if not found
        """
        # Get iteration folders in Models output directory
        iteration_dirs = [d for d in os.listdir(MODEL_FILE_PATH) if os.path.isdir(os.path.join(MODEL_FILE_PATH, d))]

        # Sort directories by creation time (ascending order)
        iteration_dirs_sorted = sorted(iteration_dirs, key=lambda f: os.path.getctime(os.path.join(MODEL_FILE_PATH, f)))

        # Check if there is at least two directories
        if len(iteration_dirs_sorted) < 2:
            print(f"ModelTrainer: Existing {model_name} not found.")
            return None

        # Get second latest directory (since latest is for newly trained models to go into)
        latest_dir = iteration_dirs_sorted[-2]

        # Load the model
        model_path = os.path.join(MODEL_FILE_PATH, latest_dir, f"{model_name.replace(' ', '_')}.pkl")
        if not os.path.exists(model_path):
            print(f"ModelTrainer: {model_name} not found at path: {model_path}")
            return None

        model = joblib.load(model_path)
        print(f"ModelTrainer: Loaded {model_name} from {model_path}")
        return model
