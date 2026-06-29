"""

Class structure of an asset used throughout the service address tracker.

"""
from dataclasses import dataclass
from service_address_tracker.constants import (
    C2MStatus, 
    MeterLocation, 
    POTHOLE_PUBLIC_MATERIALS, 
    INVALID_VALUES,
    Flag,
    FlagReason
)

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
    flag: Flag
    flag_reason: FlagReason
    
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

    def needs_followup(self, is_duplicate: bool) -> bool:
        if self.project_category == "maintenance" or (
            self.map_indy_year_built > 2015
        ) or (
            len(self.material_date_confirmation_public) > 0
        ) or (
            self.c2m_status == C2MStatus.NOT_IN_C2M
        ) or (
            self.map_indy_year_built == -1
        ) or (
            is_duplicate
        ):
            if self.project_category == "maintenance":
                self.flag_reason = FlagReason.MAINTENANCE
            elif self.map_indy_year_built > 2015:
                self.flag_reason = FlagReason.HOME_NEW
            elif len(self.material_date_confirmation_public) > 0 and not is_invalid_value(self.material_date_confirmation_public):
                self.flag_reason = FlagReason.MAT_CONF
            elif self.map_indy_year_built == -1:
                self.flag_reason = FlagReason.MISSING_MAP_INDY_YEAR
            elif is_duplicate:
                self.flag_reason = FlagReason.DUPLICATE_ADDRESS
            else:
                self.flag_reason = FlagReason.NOT_IN_C2M
            return True
        else:
            return False
        
    def needs_fireline(self) -> bool:
        return self.diameter_public > 2.0
    
def is_invalid_value(val: str) -> bool:
    return val.lower() in INVALID_VALUES