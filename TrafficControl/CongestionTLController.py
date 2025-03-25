import time

from Simulation.SimulationConfig import SUMO_STEPS_PER_SECOND
from TrafficControl import TLDensityCycleConfig as TLDensityCycleConfig
from TrafficControl.Intersection import Intersection
from TrafficControl.TLController import TLController
from TrafficControl.TLState import TLState
from TrafficControl.TrafficLightMode import TrafficLightMode


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
