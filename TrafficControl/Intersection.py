import traci

from TrafficControl.DetectorManager import DetectorManager
from Simulation.SimulationConfig import intersections_map
from TrafficControl.TLState import TLState


class Intersection:
    """
    Represents a real or SUMO (simulation) traffic intersection
    """

    def __init__(self, id: int, initial_state: TLState, initial_phase_time: float, detector_manager: DetectorManager):
        """
        Initializes an instance of an Intersection
        :param id: ID of the given intersection
        :param initial_state: Initial state of the intersection lights (TLState.py)
        :param initial_phase_time: Initial state's phase time for intersection lights
        :param detector_manager: Manages vehicle detectors corresponding to the intersection's lanes
        """
        self.id = id
        self.state = initial_state
        self.phase_time = initial_phase_time
        self.detector_manager = detector_manager

    def get_state(self) -> TLState:
        return self.state

    def get_phase_time(self) -> float:
        return self.phase_time

    def set_state(self, state: TLState):
        self.state = state

    def set_phase_time(self, phase_time: float):
        self.phase_time = phase_time

    def update(self, state: TLState, phase_time: float):
        raise NotImplementedError


class SUMOIntersection(Intersection):
    """
    Represents a SUMO (simulation) traffic intersection and its attached light(s)
    """

    def update(self, state: TLState, phase_time: float):
        """
        Updates the simulation intersections traffic lights to match the given state and phase duration
        :param state: State to update to (from TLState.py)
        :param phase_time: Duration of phase
        """
        self.state = state
        self.phase_time = phase_time
        tl_id = intersections_map.get(self.id)  # Retrieve SUMO traffic light ID from SimulationConfig.py
        try:
            traci.trafficlight.setPhase(tl_id, self.state.value)  # Set SUMO traffic light phase
            traci.trafficlight.setPhaseDuration(tl_id, self.phase_time)  # Set SUMO traffic light phase duration
        except traci.FatalTraCIError as e:
            print(f"FatalTraCIError occurred: {e}")

class ModelIntersection(Intersection):
    """
    Represents a Model (real-life) traffic intersection and its attached light(s)
    """
    def update(self, state: TLState, phase_time: float):
        pass

def IntersectionFactory(id: int, initial_state: TLState, initial_phase_time: float, detector_manager: DetectorManager, simulation_mode: bool) -> Intersection:
    """
    Initializes an instance of Intersection based on Simulation/Model mode
    :param id: ID of the given Intersection
    :param initial_state: Initial state of the intersection lights (TLState.py)
    :param initial_phase_time: Initial state's phase time for intersection lights
    :param detector_manager: DetectorManager controlling vehicle detectors corresponding to the intersection's lanes
    :param simulation_mode: True if controlling simulation, False if controlling model
    :return:
    """
    if simulation_mode:
        return SUMOIntersection(id, initial_state, initial_phase_time, detector_manager)
    else:
        return ModelIntersection(id, initial_state, initial_phase_time, detector_manager)
