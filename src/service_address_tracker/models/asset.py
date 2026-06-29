"""

Class structure of an asset used throughout the service address tracker.

"""
from dataclasses import dataclass
from service_address_tracker.constants import C2MStatus, MeterLocation, POTHOLE_PUBLIC_MATERIALS, INVALID_VALUES

@dataclass
class Asset:
    service_address: str
    project_category: str
    c2m_status: C2MStatus
    c2m_date_checked: str
    material_public: str
    material_private: str
    material_date_confirmation_public: str
    material_date_confirmation_private: str
    diameter_public: float
    diameter_private: float
    map_indy_year_built: int
    meter_location: MeterLocation
    meter_location_notes: str
    
    def needs_deletion(self) -> bool:
        return is_invalid_value(self.project_category) or len(self.project_category) == 0
    
    def needs_pothole(self) -> bool:
        return self.material_public in POTHOLE_PUBLIC_MATERIALS or (
            self.map_indy_year_built >= 1935 and self.map_indy_year_built <= 2015
            )

    def needs_replacement(self) -> bool:
        return self.map_indy_year_built < 1935 or (
            is_invalid_value(self.material_public) or len(self.material_public) == 0
            )

    def needs_followup(self) -> bool:
        return self.project_category == "maintenance" or (
            self.map_indy_year_built > 2015
        ) or (
            len(self.material_date_confirmation_public) > 0
        ) or (
            self.c2m_status == C2MStatus.NOT_IN_C2M
        ) or (
            self.map_indy_year_built == -1
        )
        
    def needs_fireline(self) -> bool:
        return self.diameter_public > 2.0
    
def is_invalid_value(val: str) -> bool:
    return val.lower() in INVALID_VALUES