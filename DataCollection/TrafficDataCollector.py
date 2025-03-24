from Config import INTERSECTION_DATA_DIR, DETECTOR_DATA_DIR, PLOT_DIR
from DataCollection.DataLogger import DataLogger


class TrafficDataCollector:
    def __init__(self):
        self.intersection_data_logger = DataLogger(INTERSECTION_DATA_DIR, PLOT_DIR)
        self.detector_data_logger = DataLogger(DETECTOR_DATA_DIR, PLOT_DIR)

    def log_intersection_data(self, intersection_data):
        """
        Logs the given intersection data to the intersection data logger
        :param intersection_data: Dictionaries of intersection information
        """
        for entry in intersection_data:
            self.intersection_data_logger.log_data(**entry)

    def log_detector_data(self, detector_data):
        """
        Logs the given detector data to the detector data logger
        :param detector_data: Dictionary of intersections and arrays of detectors
        """
        for intersection_id, detectors in detector_data.items():
            row_data = {"intersection_id": intersection_id}

            for i, detector in enumerate(detectors):
                row_data[f"detector{i}speed"] = detector["avg_vehicle_speed"]
                row_data[f"detector{i}wait"] = detector["avg_wait_time"]
                row_data[f"detector{i}vehicles"] = detector["num_vehicles"]
                row_data[f"detector{i}length"] = detector["detector_length"]

            # Log a single row per intersection
            self.detector_data_logger.log_data(**row_data)

    def end_collection(self, iteration=1):
        """
        Saves the intersection and detector log data to an iteration and time named file
        """
        self.intersection_data_logger.end_collection(f"lights_data_iter{iteration}")  # Save Intersection data log, generate plots
        self.detector_data_logger.save_log(f"detector_data_iter{iteration}")  # Save Detector data log

    def load_detector_data(self):
        """
        Loads and returns detector data for all intersections from the given file into a pandas dataframe
        :return: Pandas Dataframe of Detector Data for all intersections
        """
        return self.detector_data_logger.load_csv()


