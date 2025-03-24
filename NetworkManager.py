from Config import SIMULATION_MODE, TRAINING_MODE, ML_TRAINING_TYPE
from MachineLearning.TrainingMode import TrainingMode


class NetworkManager():
    """
    Top-level: Manages entire Traffic Control Network
    Operates simulation or physical model
    Operates machine learning if enabled
    """
    def __init__(self):
        """
        Initializes the NetworkManager with properties defined in Config.py
        """
        print("NetworkManager: Initializing Traffic Control Network...")
        if (TRAINING_MODE == True && ML_TRAINING_TYPE == None)
            print("NetworkManager: Error @Config.py: Training Mode enabled but no Training Type defined.")
        self.simulation_mode = SIMULATION_MODE
        self.training_mode = TRAINING_MODE
        self.ml_training_type = ML_TRAINING_TYPE
        print("NetworkManager: Initialized Network for " + ("simulation " if SIMULATION_MODE else
              "physical model ") + "control " + ("without model training." if TRAINING_MODE == False else
              " with " + ("supervised " if ML_TRAINING_TYPE == TrainingMode.SUPERVISED else " reinforcement ") + "training."
              ))

    def configure_network(self):
        """
        Initializes all network control structures
        """
        if (self.simulation_mode):
            self.configure_simulation_network()
        else:
            self.configure_physical_network()

    def configure_simulation_network(self):
        """
        Initializes Simulation Control Structures
        """

