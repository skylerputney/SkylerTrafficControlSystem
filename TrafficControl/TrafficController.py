from TrafficControl.TLController import TLController


class TrafficController:
    """
    Tracks and manages all TLControllers for given traffic network
    """

    def __init__(self, tl_controllers: list[TLController]):
        self.tl_controllers = tl_controllers

    def get_tl_controllers(self) -> list[TLController]:
        return self.tl_controllers

    def count_tl_controllers(self) -> int:
        return len(self.tl_controllers)

    def update(self, **kwargs):
        """
        Updates every TLController under the TrafficController
        :param kwargs: dictionary containing time_step (if defined) for simulation time management
        """
        for tl_controller in self.tl_controllers:
            tl_controller.update(**kwargs)

    def get_data(self):
        """
        Obtains data from all TLControllers
        :return: data from TLControllers
        """
        data = []
        for tl_controller in self.tl_controllers:
            data_entry = {
                "intersection_id": tl_controller.get_intersection().id,
                "state": tl_controller.get_intersection().get_state().value,
                "phase_duration": tl_controller.get_intersection().get_phase_time(),
                "current_phase_time": tl_controller.get_phase_time()
                # Add E, W, N, S wait times
            }
            data.append(data_entry)

        return data

    def get_intersection_data(self):
        """
        Obtains Intersection data from all TLControllers
        :return: Intersection data from TLControllers (Dictionary)
        """
        data = []
        for tl_controller in self.tl_controllers:
            data_entry = {
                "intersection_id": tl_controller.get_intersection().id,
                "state": tl_controller.get_intersection().get_state().value,
                "phase_duration": tl_controller.get_intersection().get_phase_time(),
                "current_phase_time": tl_controller.get_phase_time()
            }
            data.append(data_entry)

        return data

    def get_detector_data(self):
        """
        Obtains data from all Intersections' Detectors
        :return: Detector data from TLControllers' Intersections' Detectors (Dictionary Mapping of Intersection ID to Detectors' Data)
        """
        data = {}
        for tl_controller in self.tl_controllers:
            intersection_id = tl_controller.intersection.id
            detectors_data = tl_controller.intersection.detector_manager.get_detectors_data()
            data[intersection_id] = detectors_data

        return data
