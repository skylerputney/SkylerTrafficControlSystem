from TrafficControl.SUMODetector import SUMODetector


class Detector:
    """
    Represents a real or SUMO (simulation) traffic detector
    """

    def __init__(self, id: int):
        """
        Initializes an instance of a Detector
        :param id: Detector ID
        """
        self.id = id

    def get_id(self) -> int:
        return self.id

    def get_number_vehicles(self):
        raise NotImplementedError

    def get_detector_length(self):
        raise NotImplementedError

    def get_avg_vehicle_length(self):
        raise NotImplementedError

    def get_avg_vehicle_speed(self):
        raise NotImplementedError

    def get_avg_wait_time(self):
        raise NotImplementedError


def DetectorFactory(id: int, simulation_mode: bool):
    """
    Initializes an instance of Detector based on Simulation/Model mode
    :param id: ID of the given Detector
    :return:
    """
    if simulation_mode:
        return SUMODetector(id)
