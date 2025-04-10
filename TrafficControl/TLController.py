from TrafficControl.Intersection import Intersection
from TrafficControl.TrafficLightMode import TrafficLightMode
import time


class TLController():
    """
    Base class for Traffic Light Controllers
    Controls a given traffic intersection utilizing logic of the given mode
    """

    def __init__(self, intersection: Intersection, tl_mode: TrafficLightMode, simulation_mode: bool):
        """
        Initializes an instance of TLController
        :param intersection: Intersection to be controlled
        :param tl_mode: TL Operation Mode (Static, Congestion-based, AI-congestion-based)
        :param simulation_mode: True if controlling simulation, False if controlling model
        """
        self.intersection = intersection
        self.tl_mode = tl_mode
        self.simulation_mode = simulation_mode
        self.current_phase = intersection.get_state()  # Current phase
        self.phase_time = 0  # Time in current phase
        self.last_update_time = time.time() if not self.simulation_mode else 0  # Time when last phase change occurred

    def get_tl_mode(self) -> TrafficLightMode:
        return self.tl_mode

    def set_tl_mode(self, tl_mode: TrafficLightMode):
        self.tl_mode = tl_mode

    def get_intersection(self) -> Intersection:
        return self.intersection

    def get_simulation_mode(self) -> bool:
        return self.simulation_mode

    def get_phase_time(self) -> float:
        return self.phase_time

    def update(self):
        raise NotImplementedError


def TLControllerFactory(intersection: Intersection, tl_mode: TrafficLightMode, simulation_mode: bool, **kwargs) -> TLController:
    """
    Initializes an instance of TLController based on operation mode
    :param intersection: Intersection to be controlled
    :param tl_mode: TL Operation Mode (Static, Congestion-based, AI-congestion-based)
    :param simulation_mode: True if controlling simulation, False if controlling model
    :param kwargs: dictionary containing 'green_time', 'yellow_time', and 'all_red_time' if defined
            these represent static light cycle timings
    :return: TLController for given mode
    """
    from TrafficControl.AITLController import AITLController
    from TrafficControl.CongestionTLController import CongestionTLController
    from TrafficControl.StaticTLController import StaticTLController
    if tl_mode == TrafficLightMode.STATIC:
        return StaticTLController(intersection, simulation_mode, kwargs.get('green_time', 15), kwargs.get('yellow_time', 3),
                                  kwargs.get('all_red_time', 2))
    elif tl_mode == TrafficLightMode.CONGESTION_BASED:
        return CongestionTLController(intersection, tl_mode, simulation_mode)
    elif tl_mode == TrafficLightMode.AI_CONTROL:
        return AITLController(intersection, simulation_mode)
    else:
        raise ValueError(f"Invalid Traffic Light Mode: {tl_mode}")
