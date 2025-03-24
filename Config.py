import os

BASE_DIR = os.getcwd()  # Base directory for file reading, data logging
SIMULATION_CONFIG = os.path.join(BASE_DIR, "simulation_files", "simulation.sumocfg")  # Path to simulation config
SIMULATION_MODE = True  # Represents whether controlling simulation or real-world model
DATA_DIR = os.path.join(BASE_DIR, "data_logs")
PLOT_DIR = os.path.join(DATA_DIR, "plots")