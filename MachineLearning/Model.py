import os

import joblib
import numpy as np

from MachineLearning.ModelConfig import get_latest_iteration_folder
from TrafficControl.TLState import TLState


class Model:
    """
    AI Model for traffic light state and duration prediction
    """
    def __init__(self, model_name: str):
        self.model_folder = get_latest_iteration_folder()  # Path to trained model
        self.model_name = model_name  # Name of the model
        self.loaded_model = joblib.load(os.path.join(self.model_folder, self.model_name + ".pkl"))  # Loaded model

    def predict_state_and_duration(self, state: TLState, phase_duration: float, current_phase_time: float):
        """
        Passes features to model for evaluation and returns an updated state and phase duration
        :param state: Current state of the traffic intersection
        :param phase_duration: Total time of the current phase
        :param current_phase_time: Time elapsed out of phase_duration
        :return: Next phase, next phase duration
        """
        features = np.array([[state, phase_duration, current_phase_time]])  # Aggregate features to pass to model
        x, x = self.loaded_model.predict(features)
        return x
