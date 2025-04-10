import time
from MachineLearning.Model import Model
from MachineLearning.ModelConfig import AI_MODEL
from Simulation.SimulationConfig import SUMO_STEPS_PER_SECOND
from TrafficControl.Intersection import Intersection
from TrafficControl.TLController import TLController
from TrafficControl.TLDensityCycleConfig import YELLOW_CYCLE_TIME, ALL_RED_CYCLE_TIME
from TrafficControl.TLState import TLState
from TrafficControl.TrafficLightMode import TrafficLightMode


class AITLController(TLController):
    """
    AI-optimized congestion-based Traffic Light Controller
    """

    # Enforced light phase cycle (0->1->2->3->4->5->0...)
    phase_state_machine = [TLState.NSG, TLState.NSY, TLState.R, TLState.EWG, TLState.EWY, TLState.R]

    def __init__(self, intersection: Intersection, simulation_mode: bool):
        super().__init__(intersection, simulation_mode, TrafficLightMode.AI_CONTROL)
        self.model = Model(AI_MODEL)
        self.current_phase_index = self.phase_state_machine.index(self.current_phase)
        self.state_duration = 0  # How long current state should last

    def update(self, **kwargs):
        # Calculate time elapsed since last update
        current_time = kwargs.get('time_step') / SUMO_STEPS_PER_SECOND if not None else time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update current phase time
        self.phase_time += time_elapsed

        # If phase time exceeds set duration, move to next phase
        if self.phase_time >= self.state_duration:
            # Reset phase time and move to next phase
            self.phase_time = 0
            self.current_phase_index = (self.current_phase_index + 1) % len(
                self.phase_state_machine)  # Increment phase index by 1, with wrapping
            self.current_phase = self.phase_state_machine[self.current_phase_index]
            print(f"t{current_time}: Updating to {self.current_phase} for {self.get_state_duration()}")
            # Update intersection's state to reflect TLController updates
            self.intersection.update(self.current_phase, self.get_state_duration())
            self.state_duration = self.get_state_duration()  # For ML Purposes

    def get_state_duration(self) -> int:
        """
        Retrieves the static phase timing for the current state
        :return: int representing current state's static phase timing
        """
        detectorA, detectorB = (1, 3) if self.current_phase is TLState.NSG else (0, 2)
        detectorA = self.intersection.detector_manager.get_detector(detectorA)
        detectorB = self.intersection.detector_manager.get_detector(detectorB)
        if self.current_phase is TLState.NSG or self.current_phase is TLState.EWG:
            return self.model.predict_duration(detectorA.get_number_vehicles() + detectorB.get_number_vehicles(), detectorA.get_detector_length() + detectorB.get_detector_length())
        elif self.current_phase in [TLState.NSY, TLState.EWY]:
            return YELLOW_CYCLE_TIME
        elif self.current_phase is TLState.R:
            return ALL_RED_CYCLE_TIME
        else:
            raise Exception(f"Invalid TLState {self.current_phase}")