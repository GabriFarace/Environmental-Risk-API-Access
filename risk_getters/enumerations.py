from enum import Enum

class EnvironmentalRisk(Enum):
    ''' Risk levels'''
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    VERY_LOW = 1
    NO_DATA = 0


class EnvironmentalRiskType(Enum):
    '''Risk Types'''
    FLOOD_URBAN_RISK = "Flood urban risk"
    FLOOD_RIVER_RISK = "Flood river risk"
    SEISMIC_RISK = "Seismic risk"
    LANDSLIDE_RISK = "Landslide risk"


# THINK HAZARD MAP FROM THEIR TYPES TO ENUM TYPES
HAZARD_LEVEL_ENUM_MAP = {"Very low": EnvironmentalRisk.VERY_LOW, "Low": EnvironmentalRisk.LOW,
                              "Medium": EnvironmentalRisk.MEDIUM, "High": EnvironmentalRisk.HIGH}
HAZARD_TYPES_ENUM_MAP = {"River flood" : EnvironmentalRiskType.FLOOD_RIVER_RISK,
                         "Landslide" : EnvironmentalRiskType.LANDSLIDE_RISK,
                         "Urban flood" : EnvironmentalRiskType.FLOOD_URBAN_RISK,
                         "Earthquake" : EnvironmentalRiskType.SEISMIC_RISK}