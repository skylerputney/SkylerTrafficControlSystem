import traci
from Simulation.SimulationConfig import detectors_map
from TrafficControl.Detector import Detector


class SUMODetector(Detector):
    """
    Represents a SUMO (simulation) traffic detector (LaneAreaDetector, E2)
    """

    def get_number_vehicles(self):
        """
        Returns the number of vehicles on the detector in the last time step
        :return: # vehicles on detector (int)
        """
        return traci.lanearea.getLastStepVehicleNumber(self.get_sumo_id())

    def get_detector_length(self):
        """
        Returns the length of the detector in meters
        :return: length of detector (float, m)
        """
        return traci.lanearea.getLength(self.get_sumo_id())

    def get_avg_vehicle_length(self):
        """
        Returns the average length of vehicles on the detector in meters
        :return: avg. length of vehicles on detector (float, m)
        """
        vehicle_ids = self.get_vehicles_on_detector()  # Get IDs of vehicles on detector
        if len(vehicle_ids) == 0:
            return 0
        avg_length = 0
        avg_length += sum(traci.vehicle.getLength(vehicle) for vehicle in vehicle_ids)  # Sum lengths of vehicles
        avg_length /= len(vehicle_ids)  # Divide by number of vehicles to obtain average
        return avg_length

    def get_avg_wait_time(self):
        """
        Returns the average waiting time of vehicles on the detector in seconds
        :return: avg. wait time of vehicles on detector (float, s)
        """
        vehicle_ids = self.get_vehicles_on_detector()  # Get IDs of vehicles on detector
        if len(vehicle_ids) == 0:
            return 0
        avg_wait = 0
        avg_wait += sum(traci.vehicle.getWaitingTime(vehicle) for vehicle in vehicle_ids)  # Sum wait times of vehicles
        avg_wait /= len(vehicle_ids)  # Divide by number of vehicles to obtain average
        return avg_wait

    def get_max_wait_time(self):
        """
        Returns the maximum waiting time of a vehicle on the detector in seconds
        :return: max wait time of vehicle on detector (float, s)
        """
        vehicle_ids = self.get_vehicles_on_detector()  # Get IDs of vehicles on detector
        wait_times = [traci.vehicle.getWaitingTime(vehicle) for vehicle in vehicle_ids]  # Get waiting time of each vehicle
        return max(wait_times)  # Return maximum waiting time

    def get_avg_vehicle_speed(self):
        """
        Returns the average speed of vehicles on the detector in meters/s
        :return: avg. speed of vehicles on detector (float, m/s)
        """
        vehicle_ids = self.get_vehicles_on_detector()  # Get IDs of vehicles on detector
        if len(vehicle_ids) == 0:
            return 0
        avg_speed = 1e-9  # Initialize to very small value, prevent any division by 0
        avg_speed += sum(traci.vehicle.getSpeed(vehicle) for vehicle in vehicle_ids)  # Sum speed of vehicles
        avg_speed /= len(vehicle_ids)  # Divide by number of vehicles to obtain average
        return avg_speed

    def get_vehicles_on_detector(self):
        """
        Returns a list of IDs of vehicles occupying the detector
        :return: list[str] of vehicle IDs
        """
        return traci.lanearea.getLastStepVehicleIDs(self.get_sumo_id())

    def get_sumo_id(self):
        """
        Retrieve SUMO detector ID from SimulationConfig.py
        :return: detector ID (str)
        """
        return detectors_map.get(self.id)
