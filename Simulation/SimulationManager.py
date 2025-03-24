from DataCollection.TrafficDataCollector import TrafficDataCollector
from MachineLearning.ModelTrainer import ModelTrainer
from Simulation.SimulationConfig import intersections_map, intersection_detectors_map, SIMULATION_CONFIG_PATH
from Simulation.Simulation import Simulation
from TrafficControl.Detector import DetectorFactory
from TrafficControl.DetectorManager import DetectorManager
from TrafficControl.Intersection import Intersection, IntersectionFactory
from TrafficControl.TLController import TLControllerFactory
from TrafficControl.TLState import TLState
from TrafficControl.TrafficControlConfig import TRAFFIC_LIGHT_MODE
from TrafficControl.TrafficController import TrafficController

class SimulationManager:
    """
    Manages the Simulation (SUMO), TrafficController, TrafficDataCollector, and ModelTrainer interaction
    """
    def __init__(self, iterations: int):
        """
        Initializes an instance of SimulationManager
        :param iterations: Number of iterations to run the simulation
        """
        self.simulation = Simulation(SIMULATION_CONFIG_PATH)
        self.iterations = iterations
        self.current_iteration = 1
        self.time_step = 0
        self.configure_traffic_controller()
        self.data_collector = TrafficDataCollector()
        self.model_trainer = ModelTrainer()

    def configure_intersections(self) -> list[Intersection]:
        """
        Configures Intersections with their IDs and Detectors to represent SUMO intersections
        Sets intersections to have North/South Green for 15 seconds initially
        :return: List of Intersection Objects representing SUMO intersections
                contained in SimulationConfig.py
        """
        intersections = []
        for intersection in intersections_map:
            detectors = [DetectorFactory(detector_id, True) for detector_id in
                         intersection_detectors_map.get(intersection, [])]
            detector_manager = DetectorManager(detectors)
            intersections.append(IntersectionFactory(intersection, TLState.NSG, 15, detector_manager, True))
        return intersections

    def configure_traffic_controller(self):
        """
        Configures a TrafficController which contains instances of TLController for each
            SUMO intersection contained in SimulationConfig.py
        Utilizes the TrafficLightMode defined in SimulationConfig.py
        """
        intersections = self.configure_intersections()
        tl_controllers = []
        for intersection in intersections:
            tl_controllers.append(TLControllerFactory(intersection, TRAFFIC_LIGHT_MODE, True))
        self.traffic_controller = TrafficController(tl_controllers)


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





