import joblib

from TrafficControl.Intersection import Intersection
from TrafficControl.TLController import TLController
from TrafficControl.TrafficLightMode import TrafficLightMode


class AITLController(TLController):
    """
    AI-optimized congestion-based Traffic Light Controller
    """

    def __init__(self, intersection: Intersection, simulation_mode: bool, model_path: str):
        super().__init__(intersection, simulation_mode, TrafficLightMode.AI_CONTROL)
        self.model = joblib.load(model_path)
