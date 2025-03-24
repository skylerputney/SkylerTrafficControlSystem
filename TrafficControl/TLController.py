from TrafficControl.Intersection import Intersection
from Simulation.SimulationConfig import SUMO_STEPS_PER_SECOND
from TrafficControl.TLState import TLState
from TrafficControl.TrafficLightMode import TrafficLightMode
import TrafficControl.TLDensityCycleConfig as TLDensityCycleConfig
import joblib
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
        self.last_update_time = time() if not self.simulation_mode else 0  # Time when last phase change occurred

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


class CongestionTLController(TLController):
    """
    Congestion-based Traffic Light Controller
    """
    def __init__(self, intersection: Intersection, tl_mode: TrafficLightMode, simulation_mode: bool):
        super().__init__(intersection, simulation_mode, TrafficLightMode.CONGESTION_BASED)
        self.next_safe_update_time = 0  # Next time to allow safe update (after yellow/all-red phase)
        self.state_duration = 0  # Time to stay in current phase
        # Enforced light phase cycle (0->1->2->3->4->5->0...)
        self.phase_state_machine = [TLState.NSG, TLState.NSY, TLState.R, TLState.EWG, TLState.EWY, TLState.R]
        self.current_phase_index = self.phase_state_machine.index(self.current_phase)  # for state-cycling algos

    # Map of highest density lane to its green phase
    max_density_lane_phase_map = {
        0: TLState.EWG,
        2: TLState.EWG,
        1: TLState.NSG,
        3: TLState.NSG
    }

    def update(self, **kwargs):
        # Calculate time elapsed since last update
        current_time = kwargs.get('time_step') / SUMO_STEPS_PER_SECOND if not None else time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update current phase time
        self.phase_time += time_elapsed

        # Call update algorithm
        self.vehicle_count_fixed_time(current_time)

    def only_vehicle_count(self, current_time):
        lane_id, vehicle_count = self.intersection.detector_manager.get_highest_vehicle_number()
        next_green_phase = self.max_density_lane_phase_map.get(lane_id)  # Get next green phase based on highest-density lane

        # If current phase has highest density, extend time
        if self.current_phase is next_green_phase:
            self.state_duration = TLDensityCycleConfig.MIN_GREEN_CYCLE_TIME * vehicle_count
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")
            return

        # If in a yellow phase and sufficient time has passed, switch to all red
        if (self.current_phase is TLState.NSY or self.current_phase is TLState.EWY) and (self.phase_time >= self.state_duration):
            self.current_phase = TLState.R
            self.phase_time = 0
            self.state_duration = TLDensityCycleConfig.ALL_RED_CYCLE_TIME
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")
            return

        # If in a red phase and sufficient time has passed, switch to green
        if (self.current_phase is TLState.R) and (self.phase_time >= self.state_duration):
            self.current_phase = next_green_phase
            self.phase_time = 0
            self.state_duration = TLDensityCycleConfig.MIN_GREEN_CYCLE_TIME * vehicle_count
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")
            return

        # If other green phase has highest density, switch to yellow
        if self.current_phase is TLState.NSG or self.current_phase is TLState.EWG:
            yellow_phase = TLState.NSY if self.current_phase is TLState.NSG else TLState.EWY
            self.current_phase = yellow_phase
            self.phase_time = 0
            self.state_duration = TLDensityCycleConfig.YELLOW_CYCLE_TIME
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")

    def vehicle_count_fixed_time(self, current_time):
        lane_id, vehicle_count = self.intersection.detector_manager.get_highest_vehicle_number()
        next_green_phase = self.max_density_lane_phase_map.get(lane_id)  # Get next green phase based on highest-density lane

       # If cycle time not ended, pass:
        if self.phase_time < self.state_duration:
            print(f"{current_time} Passed with {self.phase_time} < {self.state_duration}")
            return

        # If in a yellow phase and sufficient time has passed, switch to all red
        if (self.current_phase is TLState.NSY or self.current_phase is TLState.EWY) and (self.phase_time >= self.state_duration):
            self.current_phase = TLState.R
            self.phase_time = 0
            self.state_duration = TLDensityCycleConfig.ALL_RED_CYCLE_TIME
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")
            return

        # If in a red phase and sufficient time has passed, switch to green
        if (self.current_phase is TLState.R) and (self.phase_time >= self.state_duration):
            self.current_phase = next_green_phase
            self.phase_time = 0
            self.state_duration = TLDensityCycleConfig.MIN_GREEN_CYCLE_TIME * vehicle_count
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")
            return

        # If other green phase has highest density, switch to yellow
        if self.current_phase is TLState.NSG or self.current_phase is TLState.EWG:
            yellow_phase = TLState.NSY if self.current_phase is TLState.NSG else TLState.EWY
            self.current_phase = yellow_phase
            self.phase_time = 0
            self.state_duration = TLDensityCycleConfig.YELLOW_CYCLE_TIME
            self.intersection.update(self.current_phase, self.state_duration)
            print(f"{current_time} Updated to {self.current_phase} for {self.state_duration}")

    def vehicle_count_fixed_time_fixed_cycle(self, current_time):
        # If phase time exceeds set duration, move to next phase
        if self.phase_time >= self.state_duration:
            # Reset phase time and move to next phase
            self.phase_time = 0
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phase_state_machine)  # Increment phase index by 1, with wrapping
            self.current_phase = self.phase_state_machine[self.current_phase_index]
            if self.current_phase is TLState.NSG or self.current_phase is TLState.EWG:
                detector = self.intersection.detector_manager.get_detector(0) if self.current_phase is TLState.EWG else self.intersection.detector_manager.get_detector(1)
                detector2 = self.intersection.detector_manager.get_detector(2) if self.current_phase is TLState.EWG else self.intersection.detector_manager.get_detector(3)
                self.state_duration = TLDensityCycleConfig.MIN_GREEN_CYCLE_TIME * max(detector.get_number_vehicles(), detector2.get_number_vehicles())
            elif self.current_phase is TLState.NSY or self.current_phase is TLState.EWY:
                self.state_duration = TLDensityCycleConfig.YELLOW_CYCLE_TIME
            else:
                self.state_duration = TLDensityCycleConfig.ALL_RED_CYCLE_TIME
            print(f"t{current_time}: Updating to {self.current_phase} for {self.state_duration}")
            # Update intersection's state to reflect TLController updates
            self.intersection.update(self.current_phase, self.state_duration)

    def vehicle_count_variable_time_fixed_cycle(self, current_time):
        # If current phase has highest density, extend it
        detector_id, num_cars = self.intersection.detector_manager.get_highest_vehicle_number()
        if (self.current_phase is TLState.NSG and (detector_id==1 or detector_id==3)) or (self.current_phase is TLState.EWG and (detector_id==0 or detector_id==2)):
            self.state_duration = TLDensityCycleConfig.MIN_GREEN_CYCLE_TIME * num_cars
            self.intersection.update(self.current_phase, self.state_duration)

        # If phase time exceeds set duration, move to next phase
        if self.phase_time >= self.state_duration:
            # Reset phase time and move to next phase
            self.phase_time = 0
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phase_state_machine)  # Increment phase index by 1, with wrapping
            self.current_phase = self.phase_state_machine[self.current_phase_index]
            if self.current_phase is TLState.NSG or self.current_phase is TLState.EWG:
                detector = self.intersection.detector_manager.get_detector(0) if self.current_phase is TLState.EWG else self.intersection.detector_manager.get_detector(1)
                detector2 = self.intersection.detector_manager.get_detector(2) if self.current_phase is TLState.EWG else self.intersection.detector_manager.get_detector(3)
                self.state_duration = TLDensityCycleConfig.MIN_GREEN_CYCLE_TIME * max(detector.get_number_vehicles(), detector2.get_number_vehicles())
            elif self.current_phase is TLState.NSY or self.current_phase is TLState.EWY:
                self.state_duration = TLDensityCycleConfig.YELLOW_CYCLE_TIME
            else:
                self.state_duration = TLDensityCycleConfig.ALL_RED_CYCLE_TIME
            print(f"t{current_time}: Updating to {self.current_phase} for {self.state_duration}")
            # Update intersection's state to reflect TLController updates
            self.intersection.update(self.current_phase, self.state_duration)

    def dynamic_state_timing(self):


        current_dir_detectors = [ 0, 1] if self.current_phase is TLState.EWG else [2, 3] if self.current_phase is TLState.NSG else None

        # If current phase has time remaining and vehicles passing in that direction, do nothing
        if self.phase_time < self.state_duration and sum(self.intersection.detector_manager.get_detector(id).get_number_vehicles() for id in current_dir_detectors) != 0:
            return

        #yellow/red log
        #if self.current_phase is TLState.NSG or se

        traffic_volumes = []
        for detector in self.intersection.detector_manager.detectors:
            MAX_NUMBER_VEHICLES = 5 if detector.id == 2 or detector.id == 3 else 3
            volume = detector.get_number_vehicles() / detector.get_detector_length()
            max_volume = MAX_NUMBER_VEHICLES / detector.get_detector_length()
            traffic_volumes.append((detector.id, volume, max_volume))

        next_phase_detector_id = max(traffic_volumes, key=lambda v: volume)
        for detector_id, volume, max_volume in traffic_volumes:
            if volume >= max_volume and detector_id is not next_phase_detector_id:
                next_phase_detector_id = detector_id
        self.current_phase = self.max_density_lane_phase_map(next_phase_detector_id)
        next_phase_detector = self.intersection.detector_manager.get_detector(next_phase_detector_id)
        self.state_duration = (next_phase_detector.get_number_vehicles() / len(traffic_volumes) * next_phase_detector.get_avg_vehicle_length() / next_phase_detector.get_avg_vehicle_speed())
        self.phase_time = 0
        self.intersection.update(self.current_phase, self.state_duration)

class AITLController(TLController):
    """
    AI-optimized congestion-based Traffic Light Controller
    """

    def __init__(self, intersection: Intersection, simulation_mode: bool, model_path: str):
        super().__init__(intersection, simulation_mode, TrafficLightMode.AI_CONTROL)
        self.model = joblib.load(model_path)


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
    if tl_mode == TrafficLightMode.STATIC:
        return StaticTLController(intersection, simulation_mode, kwargs.get('green_time', 15), kwargs.get('yellow_time', 3),
                                  kwargs.get('all_red_time', 2))
    elif tl_mode == TrafficLightMode.CONGESTION_BASED:
        return CongestionTLController(intersection, tl_mode, simulation_mode)
    elif tl_mode == TrafficLightMode.AI_CONTROL:
        return AITLController(intersection, simulation_mode)
    else:
        raise ValueError(f"Invalid Traffic Light Mode: {tl_mode}")
