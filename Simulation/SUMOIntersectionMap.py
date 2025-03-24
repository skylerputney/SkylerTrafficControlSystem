from TrafficControl.DetectorManager import DetectorManager
from TrafficControl.Intersection import Intersection, IntersectionFactory
from TrafficControl.Detector import DetectorFactory
from Simulation.SUMOIntersectionsConfig import intersections_map, intersection_detectors_map, TRAFFIC_LIGHT_MODE
from TrafficControl.TLController import TLControllerFactory
from TrafficControl.TLState import TLState
from TrafficControl.TrafficController import TrafficController

def configure_intersections() -> list[Intersection]:
    """
    Configures Intersections with their IDs and Detectors to represent SUMO intersections
    Sets intersections to have North/South Green for 15 seconds initially
    :return: List of Intersection Objects representing SUMO intersections
            contained in SUMOIntersectionsConfig.py
    """
    intersections = []
    for intersection in intersections_map:
        detectors = [DetectorFactory(detector_id, True) for detector_id in intersection_detectors_map.get(intersection, [])]
        detector_manager = DetectorManager(detectors)
        intersections.append(IntersectionFactory(intersection, TLState.NSG, 15, detector_manager, True))
    return intersections

def configure_traffic_controller() -> TrafficController:
    """
    Configures a TrafficController which contains instances of TLController for each
        SUMO intersection contained in SUMOIntersectionsConfig.py
    Utilizes the TrafficLightMode defined in SUMOIntersectionsConfig.py
    :return: TrafficController object to manage SUMO traffic intersection lights
    """
    intersections = configure_intersections()
    tl_controllers = []
    for intersection in intersections:
        tl_controllers.append(TLControllerFactory(intersection, TRAFFIC_LIGHT_MODE, True))
    return TrafficController(tl_controllers)

def main():
    ints = configure_intersections()
    print(ints.pop().detectors)

if __name__ == "__main__":
    main()