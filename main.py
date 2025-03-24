from Config import SIMULATION_CONFIG
from DataCollection.TrafficDataCollector import TrafficDataCollector
from Simulation.SUMOIntersectionMap import configure_traffic_controller
from Simulation.SimulationManager import SimulationManager


def configure_network():
    traffic_controller = configure_traffic_controller()
    traffic_data_collector = TrafficDataCollector()
    return SimulationManager(SIMULATION_CONFIG, 10, traffic_controller, traffic_data_collector)

def main():
    simulation_manager = configure_network()
    simulation_manager.run()

if __name__ == "__main__":
    main()