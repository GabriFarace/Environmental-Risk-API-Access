from abc import ABC, abstractmethod
from enumerations import EnvironmentalRiskType, EnvironmentalRisk

class RiskGetter(ABC):

    @abstractmethod
    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the environmental risk associated to the given longitude and latitude.'''
        pass



class RiskManager:
    ''' The Risk Manager deals with the different risk getters and return the risk indicators for each risk type'''
    def __init__(self, risk_getters_per_type: dict[EnvironmentalRiskType, list[RiskGetter]]):

        # For each risk type there is a list of list getters
        self.risk_getters_per_type = risk_getters_per_type

    def get_indicators(self, longitude: float, latitude: float) -> dict[EnvironmentalRiskType, EnvironmentalRisk]:
        ''' Return the risk indicators, for each risk type, associated to the location with the given longitude and latitude.
            The RiskManager will try to take the risk indicator (level) for each risk type until the list ends. In these way the
            the manager can deal with getters that do not provide risk data for that particular location
        '''

        # Fetch the risk indicator for each risk type until one getter has data associated to it
        result = {}
        for risk_type in self.risk_getters_per_type.keys():

            for getter in self.risk_getters_per_type[risk_type]:

                risk_indicator = getter.get_risk(longitude, latitude)

                if risk_indicator != EnvironmentalRisk.NO_DATA:
                    result[risk_type] = risk_indicator
                    break

            if not risk_type in result.keys():
                result[risk_type] = EnvironmentalRisk.NO_DATA

        return result

