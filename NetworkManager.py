from Config import SIMULATION_MODE, TRAINING_MODE, ML_TRAINING_TYPE, NUM_SIM_ITERATIONS
from MachineLearning.TrainingMode import TrainingMode
from RLModel.RLModelManager import RLModelManager
from Simulation.SimulationManager import SimulationManager


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
        if TRAINING_MODE and ML_TRAINING_TYPE is None:
            print("NetworkManager: Error @Config.py: Training Mode enabled but no Training Type defined.")
        self.simulation_mode = SIMULATION_MODE
        self.training_mode = TRAINING_MODE
        self.ml_training_type = ML_TRAINING_TYPE
        print("NetworkManager: Initialized Network for " + ("simulation " if SIMULATION_MODE else
              "physical model ") + "control " + ("without model training." if not TRAINING_MODE else
              " with " + ("supervised " if ML_TRAINING_TYPE == TrainingMode.SUPERVISED else " reinforcement ") + "training."
              ))
        self.configure_network()

    def configure_network(self):
        """
        Initializes all network control structures
        """
        if self.simulation_mode:
            self.configure_simulation_network()
        else:
            self.configure_physical_network()

    def configure_simulation_network(self):
        """
        Initializes Simulation Control Structures
        """
        self.manager = SimulationManager(NUM_SIM_ITERATIONS)

    def configure_physical_network(self):
        self.manager = RLModelManager()

    def start(self):
        """
        Starts the traffic control network
        """
        print("NetworkManager: Starting Traffic Control Network...")
        self.manager.run()

