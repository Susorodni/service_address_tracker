from enum import Enum
from typing import List

POTHOLE_PUBLIC_MATERIALS = {
    "copper",
    "polyethylene"
}

INVALID_VALUES = [
    "null",
    "<null>",
    "nan"
]

SUPPORTED_FILE_EXTENSIONS = [
    "*.xls",
    "*.xlsx",
    "*.xlsm",
    "*.xlsb",
    "*.odf",
    "*.ods",
    "*.odt",
    "*.csv"
]

SUPPORTED_FILETYPE_DROPDOWNS: List[tuple[str, str | list[str] | tuple[str, ...]]] = [
    ("All supported filetypes", SUPPORTED_FILE_EXTENSIONS),
    ("Excel Files", SUPPORTED_FILE_EXTENSIONS[0:-1]),
    ("CSV Files", SUPPORTED_FILE_EXTENSIONS[-1])
]

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
    
class Flag(Enum):
    FIRE_LINE = "Fire Line"
    NEEDS_POTHOLED = "Needs to be Potholed"
    REPLACEMENT = "Replacement"
    FOLLOW_UP = "Follow Up"

class FlagReason(Enum):
    SAFE_PUB_MAT = "Public material is either Copper or Polyethylne"
    HOME_OLD = "Home was built before 1935"
    HOME_MED = "Home was built between 1935 and 2015"
    HOME_NEW = "Home was built during or after 2016"
    MISSING_MAT = "Public material is null or blank"
    MAINTENANCE = "Type of Service Replacement is Maintenance"
    MAT_CONF = "Public Date of Material Confirmation is populated"
    NOT_IN_C2M = "C2M Status is NotInC2M"
    MISSING_MAP_INDY_YEAR = "Map Indy Year Built is XXXX"
    DUPLICATE_ADDRESS = "Duplicate Service Address"
    LARGE_DIAMETER = "Service line has a diameter > 2 inches"