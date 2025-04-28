from Communication.PLC import PLC
from Communication.PLCConfig import TRAFFIC_PLC_IP_ADDRESS
from RLModel.RLModelConfig import rl_intersections_map
from TrafficControl.SUMOIntersection import SUMOIntersection
from TrafficControl.TLState import TLState


class HybridIntersection(SUMOIntersection):
    """
    Represents a SUMO (simulation) and real-world traffic intersection and its attached light(s)
    """

    def __init__(self, id, initial_state, initial_phase_time, detector_manager):
        super().__init__(id, initial_state, initial_phase_time, detector_manager)
        self.plc = PLC(TRAFFIC_PLC_IP_ADDRESS)
        self.plc.connect()

    def update(self, state: TLState, phase_time: float):
        super().update(state, phase_time)  # Update SUMO
        try:
            plc_tag = rl_intersections_map.get(self.id)
            self.plc.write_tag(plc_tag + "_DATA[5]", state.value)  # Update PLC (Full OPC control mode)
        except Exception as e:
            print(f"PLC update failed: {e}")

