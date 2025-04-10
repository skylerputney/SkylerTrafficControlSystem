import os
from MachineLearning.TrainingMode import TrainingMode

SIMULATION_MODE = True  # Represents whether controlling simulation or real-world model
RUN_MODEL_ON_SIM = True  # Represents whether to run the real-world model based on the simulation traffic
TRAINING_MODE = False  # Represents whether using data to train models
ML_TRAINING_TYPE = TrainingMode.SUPERVISED  # Represents whether using Supervised or Reinforcement Learning (None if not training)
NUM_SIM_ITERATIONS = 1  # Number of iterations to run the simulation for

BASE_DIR = os.getcwd()  # Base directory for file reading, data logging
DATA_DIR = os.path.join(BASE_DIR, "data_logs")
PLOT_DIR = os.path.join(DATA_DIR, "plots")
INTERSECTION_DATA_DIR = os.path.join(DATA_DIR, "intersections")
DETECTOR_DATA_DIR = os.path.join(DATA_DIR, "detectors")
