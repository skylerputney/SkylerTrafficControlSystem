from TrafficControl.Detector import Detector


class DetectorManager:
    """
    Tracks and manages all Detectors for a given traffic Intersection
    """

    def __init__(self, detectors: list[Detector]):
        self.detectors = detectors

    def get_detector(self, detector_id):
        return self.detectors[detector_id]

    def get_highest_wait_time(self):
        """
        Returns the ID and wait time of the detector with the highest vehicle waiting time
        :return: detector id (int), max recorded wait time (float, s)
        """
        highest_detector = max(self.detectors, key=lambda d: d.get_max_wait_time())  # Find detector with highest wait time
        return highest_detector.get_id(), highest_detector.get_max_wait_time()

    def get_highest_vehicle_number(self):
        """
        Returns the ID and number of vehicles of the detector with the highest number of vehicles present
        :return: detector id (int), # vehicles (int)
        """
        highest_detector = max(self.detectors, key=lambda d: d.get_number_vehicles())  # Find detector with highest vehicle number
        return highest_detector.get_id(), highest_detector.get_number_vehicles()

    def get_detectors_data(self):
        """
        Returns Array of Dictionaries containing all data for each detector
        :return: Detectors' Data (Array of Dictionaries)
        """
        data = []
        for detector in self.detectors:
            data_entry = {
                "detector_id": detector.get_id(),
                "num_vehicles": detector.get_number_vehicles(),
                "avg_vehicle_speed": detector.get_avg_vehicle_speed(),
                "avg_wait_time": detector.get_avg_wait_time(),
                "detector_length": detector.get_detector_length()
            }
            data.append(data_entry)

        return data
