import os
from datetime import datetime
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from xgboost.testing.data import joblib
import joblib
from Config import DATA_DIR, ML_TRAINING_TYPE
from FileManager.FileManager import FileManager
from MachineLearning.ModelConfig import get_latest_dataset, MODELS, PARAM_GRIDS
from MachineLearning.TrainingMode import TrainingMode


class ModelTrainer:
    """
    Trains and evaluates Machine Learning Models using latest simulation data
    """
    def __init__(self, iteration=1):
        self.iteration = iteration  # Iteration of consecutive training
        self.training_data_path = get_latest_dataset()

    def train_test_model(self, iteration=1):
        raise NotImplementedError


def ModelTrainerFactory(iteration: int=1) -> ModelTrainer:
    """
    Initializes an instance of ModelTrainer based on ML_TRAINING_TYPE (Config.py)
    :param iteration: Iteration # of consecutive training
    :return: ModelTrainer
    """
    from MachineLearning.ReinforcementModelTrainer import ReinforcementModelTrainer
    from MachineLearning.SupervisedModelTrainer import SupervisedModelTrainer
    return SupervisedModelTrainer(iteration) if ML_TRAINING_TYPE is TrainingMode.SUPERVISED else ReinforcementModelTrainer(iteration)

