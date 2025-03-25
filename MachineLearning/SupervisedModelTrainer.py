from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from Config import DATA_DIR, INTERSECTION_DATA_DIR, DETECTOR_DATA_DIR
from FileManager.FileManager import FileManager
from MachineLearning.ModelConfig import SUPERVISED_MODEL_FILE_PATH
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

    def train_models(self, iteration=1):


