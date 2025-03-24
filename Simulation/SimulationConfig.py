import os
from Config import BASE_DIR

# Whether to open simulation GUI
SUMO_GUI = False

# Simulation Config Path
SIMULATION_CONFIG_PATH = os.path.join(BASE_DIR, "simulation_files", "simulation.sumocfg")

# Timing adjustment for SUMO steps v. seconds
SUMO_STEPS_PER_SECOND = 2

# Map of intersection id to SUMO network.net.xml ID
intersections_map = {
    0: "1120209834"
}

# Map of detector id to SUMO detector.add.xml ID
detectors_map = {
    0: "detector_west_8",
    1: "detector_south_2",
    2: "detector_east_5",
    3: "detector_north_4"
}

# Map of intersection(s) to detector(s)
intersection_detectors_map = {
    0: [0, 1, 2, 3]  # Intersection 0 has detectors 0-3
}