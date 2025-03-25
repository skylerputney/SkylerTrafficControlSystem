import traci

from Simulation.SimulationConfig import intersections_map
from TrafficControl.Intersection import Intersection
from TrafficControl.TLState import TLState


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
