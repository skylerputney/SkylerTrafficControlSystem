from enum import Enum

class TrafficLightMode(Enum):
    """
    Enumeration of values to represent various light control modes
    """
    STATIC = 0            # Static light timings (15G->3Y->2R->15R->3Y->2R->15G->...)
    CONGESTION_BASED = 1  # Congestion-based light timings (If/Else)
    AI_CONTROL = 2        # AI-optimized congestion-based light timings
