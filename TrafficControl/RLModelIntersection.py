from TrafficControl.Intersection import Intersection
from TrafficControl.TLState import TLState


class ModelIntersection(Intersection):
    """
    Represents a Model (real-life) traffic intersection and its attached light(s)
    """
    def update(self, state: TLState, phase_time: float):
        pass
