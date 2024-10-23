from abc import ABC, abstractmethod
from utility.enumerations import EnvironmentalRisk

class RiskGetter(ABC):

    @abstractmethod
    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the environmental risk associated to the given longitude and latitude.'''
        pass
