from enum import Enum
from flood_risk_getters import FloodRiskGetter
from landslide_risk_getters import LandslideRiskGetter
from seismic_risk_getters import SeismicRiskGetter

class EnvironmentalRisk(Enum):
    ''' Risk levels'''
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    VERY_LOW = 1
    NO_DATA = 0


class EnvironmentalRiskType(Enum):
    '''Risk Types'''
    FLOOD_URBAN_RISK = FloodRiskGetter
    FLOOD_RIVER_RISK = FloodRiskGetter
    SEISMIC_RISK = SeismicRiskGetter
    LANDSLIDE_RISK = LandslideRiskGetter


# THINK HAZARD MAP FROM THEIR TYPES TO ENUM TYPES
HAZARD_LEVEL_ENUM_MAP = {"Very Low": EnvironmentalRisk.VERY_LOW, "Low": EnvironmentalRisk.LOW,
                              "Medium": EnvironmentalRisk.MEDIUM, "High": EnvironmentalRisk.HIGH}
HAZARD_TYPES_ENUM_MAP = {"River flood" : EnvironmentalRiskType.FLOOD_RIVER_RISK,
                         "Landslide" : EnvironmentalRiskType.LANDSLIDE_RISK,
                         "Urban flood" : EnvironmentalRiskType.FLOOD_URBAN_RISK,
                         "Earthquake" : EnvironmentalRiskType.SEISMIC_RISK}