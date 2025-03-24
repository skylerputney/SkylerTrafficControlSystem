from DataCollection.TrafficDataCollector import TrafficDataCollector
from MachineLearning.ModelTrainer import ModelTrainer
from Simulation.Simulation import Simulation
from TrafficControl.TrafficController import TrafficController


class SimulationManager:
    """
    Manages the Simulation (SUMO), Traffic Controller, TrafficDataCollector, and ModelTrainer interaction
    """
    def __init__(self, sumo_config_path: str, iterations: int, traffic_controller: TrafficController, data_collector: TrafficDataCollector):
        """
        Initializes an instance of SimulationManager
        :param sumo_config_path: Path to SUMO configuration file
        :param iterations: Number of iterations to run the simulation
        :param traffic_controller: TrafficController to modify simulation traffic lights
        """
        self.simulation = Simulation(sumo_config_path)
        self.iterations = iterations
        self.current_iteration = 1
        self.traffic_controller = traffic_controller
        self.data_collector = data_collector
        self.time_step = 0
        self.model_trainer = ModelTrainer()

    def run(self):
        """
        Runs the simulation to completion self.iterations times
        Uses TrafficController to update simulation traffic lights
        """
        while self.current_iteration <= self.iterations:
            self.simulation.start()
            while self.simulation.get_vehicle_number() > 0:
                self.traffic_controller.update(time_step=self.time_step)
                self.data_collector.log_intersection_data(self.traffic_controller.get_intersection_data())
                self.data_collector.log_detector_data(self.traffic_controller.get_detector_data())
                self.simulation.step()
                self.time_step += 1
            self.simulation.end()
            self.data_collector.end_collection(self.current_iteration)
            self.model_trainer.train_models(iteration=self.current_iteration)
            self.current_iteration += 1





