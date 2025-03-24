import traci

from Simulation.SimulationConfig import SUMO_GUI

TRAFFIC_GEN_SCALE = 1

class Simulation:
    """
    Represents a SUMO (Simulation of Urban MObility) instance
    """

    def __init__(self, sumo_config_path: str):
        """
        Creates an instance of a SUMO (Simulation of Urban MObility) simulation
        :param sumo_config_path: Path to SUMO configuration file
        """
        self.sumo_config_path = sumo_config_path

    def start(self):
        """
        Starts a SUMO simulation from the given configuration file with a GUI
        """
        sumo_cmd = ["sumo-gui" if SUMO_GUI else "sumo", "-c", self.sumo_config_path, "--tripinfo-output", "tripinfo.xml", "--scale", str(TRAFFIC_GEN_SCALE)]  # Sumo Arguments: launch with GUI, config file, tripinfo output file, traffic generation scale (0-1)
        traci.start(sumo_cmd)

    def step(self):
        """
        Steps the simulation forward once
        """
        try:
            traci.simulationStep()
        except traci.FatalTraCIError as e:
            print(f"FatalTraCIError occurred: {e}")

    def end(self):
        """
        Ends the simulation
        """
        traci.close()

    def get_vehicle_number(self):
        """
        :return: Number of vehicles left in simulation
        """
        return traci.simulation.getMinExpectedNumber()


