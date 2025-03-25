import time
from Simulation.SimulationConfig import SUMO_STEPS_PER_SECOND
from TrafficControl.Intersection import Intersection
from TrafficControl.TLController import TLController
from TrafficControl.TLState import TLState
from TrafficControl.TrafficLightMode import TrafficLightMode


class StaticTLController(TLController):
    """
    Static-Timing Traffic Light Controller
    """

    # Enforced light phase cycle (0->1->2->3->4->5->0...)
    phase_state_machine = [TLState.NSG, TLState.NSY, TLState.R, TLState.EWG, TLState.EWY, TLState.R]

    def __init__(self, intersection: Intersection, simulation_mode: bool, green_time: int = 15, yellow_time: int = 3, all_red_time: int = 2):
        """
        Initialize an instance of a Static Traffic Light Controller
        :param intersection: Intersection to be controlled
        :param green_time: Green light timing (default: 15s)
        :param yellow_time: Yellow light timing (default: 3s)
        :param all_red_time: All Red transitional light timing (default: 2s)
        """
        super().__init__(intersection, TrafficLightMode.STATIC, simulation_mode)
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.all_red_time = all_red_time
        self.current_phase_index = self.phase_state_machine.index(self.current_phase)

    def update(self, **kwargs):
        """
        Update Traffic Light state based on defined phase_state_machine and given static timings
        :param kwargs: dictionary containing a 'time_step' argument (if defined) that represents
                simulation time (in s) when divided by SUMO_STEPS_PER_SECOND (from SimulationConfig.py)
                Utilized to track simulation time
        """
        # Calculate time elapsed since last update
        current_time = kwargs.get('time_step') / SUMO_STEPS_PER_SECOND if not None else time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update current phase time
        self.phase_time += time_elapsed

        # If phase time exceeds set duration, move to next phase
        if self.phase_time >= self.get_state_duration():
            # Reset phase time and move to next phase
            self.phase_time = 0
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phase_state_machine)  # Increment phase index by 1, with wrapping
            self.current_phase = self.phase_state_machine[self.current_phase_index]
            print(f"t{current_time}: Updating to {self.current_phase} for {self.get_state_duration()}")
            # Update intersection's state to reflect TLController updates
            self.intersection.update(self.current_phase, self.get_state_duration())

    def get_state_duration(self) -> int:
        """
        Retrieves the static phase timing for the current state
        :return: int representing current state's static phase timing
        """
        if self.current_phase in [TLState.NSG, TLState.EWG]:
            return self.green_time
        elif self.current_phase in [TLState.NSY, TLState.EWY]:
            return self.yellow_time
        elif self.current_phase is TLState.R:
            return self.all_red_time
        else:
            raise Exception(f"Invalid TLState {self.current_phase}")
