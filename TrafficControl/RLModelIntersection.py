from Communication.PLC import PLC
from Communication.PLCConfig import TRAFFIC_PLC_IP_ADDRESS
from RLModel.RLModelConfig import rl_intersections_map
from TrafficControl.DetectorManager import DetectorManager
from TrafficControl.Intersection import Intersection
from TrafficControl.TLState import TLState


class ModelIntersection(Intersection):
    """
    Represents a Model (real-life) traffic intersection and its attached light(s)
    """

    def __init__(self, id: int, initial_state: TLState, initial_phase_time: float, detector_manager: DetectorManager):
        super().__init__(id, initial_state, initial_phase_time, detector_manager)
        self.plc = PLC(TRAFFIC_PLC_IP_ADDRESS)
        self.plc.connect()


    def update(self, state: TLState, phase_time: float):
        """
        Updates the real-world model intersections' traffic lights to match the given state and phase duration
        :param state: State to update to (from TLState.py)
        :param phase_time: Duration of phase
        """
        self.state = state
        self.phase_time = phase_time
        #plc = PLC(TRAFFIC_PLC_IP_ADDRESS)
        #plc.connect()
        plc_tag = rl_intersections_map.get(self.id)
        self.plc.write_tag(plc_tag + "_DATA[5]", state.value)

