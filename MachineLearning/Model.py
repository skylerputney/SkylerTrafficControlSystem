import os

import joblib
import numpy as np

from FileManager.FileManager import FileManager
from MachineLearning.ModelConfig import get_latest_iteration_folder, SUPERVISED_MODEL_FILE_PATH
from Simulation.SimulationConfig import TRAFFIC_GEN_SCALE
from TrafficControl.TLState import TLState


class Model:
    """
    AI Model for traffic light state and duration prediction
    """
    def __init__(self, model_name: str):
        self.model_manager = FileManager(SUPERVISED_MODEL_FILE_PATH)  # Path to trained model
        self.model_name = model_name  # Name of the model
        latest_sub_dir = self.model_manager.get_latest_sub_dir()
        self.loaded_model = self.model_manager.load_pkl(self.model_name + ".pkl", latest_sub_dir)
        print(f"Model: Loaded {model_name} from {latest_sub_dir}")

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

    def predict_duration(self, vehicle_count, detector_length):
        features = np.array([[vehicle_count, detector_length, TRAFFIC_GEN_SCALE]])
        Y = self.loaded_model.predict(features)
        return Y[0]

