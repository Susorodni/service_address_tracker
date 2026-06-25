"""

Class structure of an asset used throughout the service address tracker.

"""
from dataclasses import dataclass
from enum import Enum

class C2MStatus(Enum):
    ACTIVE = "Active"
    NOT_IN_C2M = "Not in C2M"
    OFF = "Off"
    DISCONNECTED = "Disconnected"
    
class MeterLocation(Enum):
    BASEMENT_1 = "Basement 1"
    BASEMENT_2 = "Basement 2"
    BASEMENT_3 = "Basement 3"
    BASEMENT_4 = "Basement 4"
    BASEMENT_5 = "Basement 5"
    BASEMENT_6 = "Basement 6"
    BASEMENT_7 = "Basement 7"
    BASEMENT_8 = "Basement 8"
    PIT_0 = "Pit 0"
    PIT_1 = "Pit 1"
    PIT_2 = "Pit 2"
    PIT_3 = "Pit 3"
    PIT_4 = "Pit 4"
    PIT_5 = "Pit 5"
    PIT_6 = "Pit 6"
    PIT_7 = "Pit 7"
    PIT_8 = "Pit 8"
    PIT_9 = "Pit 9"

@dataclass
class Asset:
    service_address: str
    c2m_status: C2MStatus
    c2m_date_checked: str
    material_public: str
    material_private: str
    material_date_confirmation_public: str
    material_date_confirmation_private: str
    diameter_public: float
    diameter_private: float
    map_indy_year_built: str
    meter_location: MeterLocation
    meter_location_notes: str
