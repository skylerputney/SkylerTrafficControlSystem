from Config import ML_TRAINING_TYPE
from MachineLearning.TrainingMode import TrainingMode


class ModelTrainer:
    """
    Trains and evaluates Machine Learning Models using latest simulation data
    """
    def __init__(self, iteration=1):
        self.iteration = iteration  # Iteration of consecutive training
        self.training_data_path = None

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

