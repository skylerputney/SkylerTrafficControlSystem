from datetime import datetime

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

from Config import DATA_DIR, INTERSECTION_DATA_DIR, DETECTOR_DATA_DIR
from FileManager.FileManager import FileManager
from MachineLearning.ModelConfig import SUPERVISED_MODEL_FILE_PATH, MODELS, PARAM_GRIDS
from MachineLearning.ModelTrainer import ModelTrainer


class SupervisedModelTrainer(ModelTrainer):
    """
    Trains Supervised Learning Models
    """
    def __init__(self):
        self.intersection_data_manager = FileManager(INTERSECTION_DATA_DIR)
        self.detector_data_manager = FileManager(DETECTOR_DATA_DIR)
        self.model_manager = FileManager(SUPERVISED_MODEL_FILE_PATH)

    def get_phase_model_features_and_targets(self):
        """
        Defines features (X) and target variables (Y) for Phase Selection Model training
        Splits the data into training and testing sets, scales features
        :return: X_train_scaled, X_test_scaled, Y_train, Y_test
        """
        # Read in data
        data = self.intersection_data_manager.load_latest_csv()

        # Define features (X) and target variables (Y)
        X = data[['state', 'phase_duration', 'current_phase_time']]
        Y = data[['state']]

        return self.split_and_scale_data(X, Y)

    def get_duration_model_features_and_targets(self):
        """
        Defines features (X) and target variables (Y) for Phase Duration Model training
        Splits the data into training and testing sets, scales features
        :return: X_train_scaled, X_test_scaled, Y_train, Y_test
        """
        # Read in data
        data = self.detector_data_manager.load_latest_csv()

        # Define features (X) and target variables (Y)
        X = data[[]]
        Y = data[[]]

        return self.split_and_scale_data(X, Y)

    def split_and_scale_data(self, X, Y):
        """
        Splits data into training and testing sets and scales features
        :param X: Features
        :param Y: Target Variables
        :return: X training and testing scaled, Y training and testing
        """
        # Split data into training and testing sets
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.fit_transform(X_test)

        return X_train_scaled, X_test_scaled, Y_train, Y_test

    def hyperparameter_tuning(self, model, model_name, X_train, Y_train):
        """
        Peforms hyperparameter tuning on models that need it and fits models that don't
        :param model: Model to tune/fit
        :param model_name: Model name
        :param X_train: Training features
        :param Y_train: Training target variables
        :return: Tuned/Fitted model
        """
        if model_name in PARAM_GRIDS:
            grid_search = GridSearchCV(model, PARAM_GRIDS[model_name], cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
            grid_search.fit(X_train, Y_train.values.ravel())
            model = grid_search.best_estimator_
            print(f"SupervisedModelTrainer: Best parameters for {model_name}: {grid_search.best_params_}")
        else:
            model.fit(X_train, Y_train.values.ravel())

        return model


    def train_duration_model(self, iteration=1):
        # Update iteration number
        self.iteration = iteration

        # Get latest existing model directory
        latest_model_dir = self.model_manager.get_latest_sub_dir()

        # Create model output directory
        model_output_dir = self.model_manager.create_sub_dir(f"iteration{self.iteration}_{datetime.now().strftime('%Y%m%d%H%M%S')}")

        # Get features and targets
        X_train, X_test, Y_train, Y_test = self.get_duration_model_features_and_targets()

        # Loop through MODELS defined in ModelConfig.py and train them based on latest data
        for model_name, model in MODELS.items():

            # Load the most recent model iteration, if exists, else initialize new model
            model_file_name = f"{model_name.replace(' ', '_')}.pkl"
            loaded_model = self.model_manager.load_pkl(model_file_name, latest_model_dir)
            model = loaded_model if loaded_model is not None else model
            print("SupervisedModelTrainer: Training " + "new " if not loaded_model else "loaded " +
                  f"{model_name} " + "model" + f" loaded from {latest_model_dir}" if loaded_model else ".")

            # Hyperparameter tuning / Fitting
            model = self.hyperparameter_tuning(model, model_name, X_train, Y_train)

            # Save trained model
            model_path = self.model_manager.save_pkl(model, model_file_name, model_output_dir)
            print(f"SupervisedModelTrainer: {model_name} saved to {model_path}.")



