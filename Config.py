import os
from MachineLearning.TrainingMode import TrainingMode

SIMULATION_MODE = True  # Represents whether controlling simulation or real-world model
TRAINING_MODE = True  # Represents whether using data to train models
ML_TRAINING_TYPE = TRAINING_MODE.SUPERVISED  # Represents whether using Supervised or Reinforcement Learning (None if not training)

BASE_DIR = os.getcwd()  # Base directory for file reading, data logging
SIMULATION_CONFIG = os.path.join(BASE_DIR, "simulation_files", "simulation.sumocfg")  # Path to simulation config
DATA_DIR = os.path.join(BASE_DIR, "data_logs")
PLOT_DIR = os.path.join(DATA_DIR, "plots")
INTERSECTION_DATA_DIR = os.path.join(DATA_DIR, "intersections")
DETECTOR_DATA_DIR = os.path.join(DATA_DIR, "detectors")
