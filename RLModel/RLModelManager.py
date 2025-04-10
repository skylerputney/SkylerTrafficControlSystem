from RLModel.RLModelConfig import intersection_detectors_map, rl_intersections_map
from TrafficControl.Detector import DetectorFactory
from TrafficControl.DetectorManager import DetectorManager
from TrafficControl.Intersection import Intersection, IntersectionFactory
from TrafficControl.TLController import TLControllerFactory
from TrafficControl.TLState import TLState
from TrafficControl.TrafficControlConfig import TRAFFIC_LIGHT_MODE
from TrafficControl.TrafficController import TrafficController


class RLModelManager():
    """
    Manages the Physical Model, TrafficController, and TrafficDataCollector interaction
    """
    def __init__(self):
        self.configure_traffic_controller()

    def configure_intersections(self) -> list[Intersection]:
        """
        Configures Intersections with their IDs and Detectors to represent SUMO intersections
        Sets intersections to have North/South Green for 15 seconds initially
        :return: List of Intersection Objects representing SUMO intersections
                contained in SimulationConfig.py
        """
        intersections = []
        for intersection in rl_intersections_map:
            detectors = [DetectorFactory(detector_id, True) for detector_id in
                         intersection_detectors_map.get(intersection, [])]
            detector_manager = DetectorManager(detectors)
            intersections.append(IntersectionFactory(intersection, TLState.NSG, 15, detector_manager, False))
        return intersections
    def configure_traffic_controller(self):
        intersections = self.configure_intersections()
        tl_controllers = []
        for intersection in intersections:
            tl_controllers.append(TLControllerFactory(intersection, TRAFFIC_LIGHT_MODE, False))
        self.traffic_controller = TrafficController(tl_controllers)
    def run(self):
        while True:
            self.traffic_controller.update()
