from enum import Enum


class TLState(Enum):
    """
    Enumeration of values to represent various intersection light phases
    Matches PLC and SUMO phase indices
    """
    NSG = 0  # North/South Green, East/West Red
    NSY = 1  # North/South Yellow, East/West Red
    EWG = 2  # East/West Green, North/South Red
    EWY = 3  # East/West Yellow, North/South Red
    R = 4  # All Red

