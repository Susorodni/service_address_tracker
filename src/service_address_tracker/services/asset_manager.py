# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:27:04 2026

@author: c10265
"""

import re
import pandas as pd
from service_address_tracker.models.asset import Asset
from service_address_tracker.utils import parse_inches_2, parse_map_indy
from service_address_tracker.constants import C2MStatus, MeterLocation, Flag, FlagReason


def build_assets(df: pd.DataFrame) -> list[Asset]:
    """

    Builds the imported DataFrame into a list of Assets that follow the proper
    data types for each column.

    Args:
        df (DataFrame): the DataFrame that the Assets will be taken from

    Raises:
        e: any exception raised

    Returns:
        list[Asset]: the list of processed Assets
    """

    # Grab only the columns that correspond to data that will either be used,
    # or presented in the final output.
    df = df.filter([
        "Service Address",
        "Type of Service Replacement (Project Category)",
        "C2M Status",
        "Date Checked in C2M",
        "Public Material",
        "Public Date of Material Confirmation",
        "Public Diameter",
        "Private Material",
        "Private Date of Material Confirmation",
        "Private Diameter",
        "Map Indy Year Built",
        "Meter Location",
        "Meter Location Notes"
        ], axis=1)

    # Fill any public/private diameter, map indy year with -1 if a "na" value
    # df["Public Diameter"] = df["Public Diameter"].fillna(-1)
    # df["Private Diameter"] = df["Private Diameter"].fillna(-1)
    

    # Removes duplicate service addresses. Does not account for duplicate
    # owner names or contact information on related, but not exact,
    # service addresses.
    records = df.to_dict("records")
    # print(records)

    assets = []

    for r in records:
        try:
            asset = Asset(
                service_address=str(r.get("Service Address")),
                project_category=str(r.get(
                    "Type of Service Replacement (Project Category)"
                )),
                c2m_status=match_c2m_status(str(r.get(
                    "C2M Status"
                ))),
                c2m_date_checked=str(r.get(
                    "Date Checked in C2M"
                )),
                material_public=str(r.get(
                    "Public Material"
                )),
                material_private=str(r.get(
                    "Private Material"
                )),
                material_date_confirmation_public=str(r.get(
                    "Public Date of Material Confirmation"
                )),
                material_date_confirmation_private=str(r.get(
                    "Private Date of Material Confirmation"
                )),
                diameter_public=parse_inches_2(str(r.get(
                    "Public Diameter"
                ))),
                diameter_private=parse_inches_2(str(r.get(
                    "Private Diameter"
                ))),
                map_indy_year_built=parse_map_indy(str(r.get(
                    "Map Indy Year Built"
                ))),
                meter_location=match_meter_location(str(r.get(
                    "Meter Location"
                ))),
                meter_location_notes=str(r.get(
                    "Meter Location Notes"
                )),
                flag=Flag.NONE,
                flag_reason=FlagReason.NONE
                )
            assets.append(asset)
        except Exception as e:
            print(f"Error for value {r}")
            raise e


    return assets

def sort_assets(assets: list[Asset]) -> list[Asset]:
    
    unq_street_address = []
    
    for a in assets:
        
        is_duplicate = a.service_address in unq_street_address
        
        if a.needs_deletion():
            a.flag = Flag.DELETE
        elif a.needs_fireline():
            a.flag = Flag.FIRE_LINE
        elif a.needs_pothole():
            a.flag = Flag.NEEDS_POTHOLED
        elif a.needs_replacement():
            a.flag = Flag.REPLACEMENT
        elif a.needs_followup(is_duplicate):
            a.flag = Flag.FOLLOW_UP
        else:
            raise ValueError("Invalid flag configuration")
        
        unq_street_address.append(a.service_address)
        
    return assets
            

def str_trim(s: str) -> str:
    return re.sub(r"\s+", "", s).lower()

def match_c2m_status(s: str) -> C2MStatus:
    s_test = str_trim(s)
    
    match s_test:
        case "active":
            return C2MStatus.ACTIVE
        case "off":
            return C2MStatus.OFF
        case "disconnected":
            return C2MStatus.DISCONNECTED
        case _:
            return C2MStatus.NOT_IN_C2M
        
def match_meter_location(s: str) -> MeterLocation:
    s_test = str_trim(s)
    
    match s_test:
        case "basement1":
            return MeterLocation.BASEMENT_1
        case "basement2":
            return MeterLocation.BASEMENT_2
        case "basement3":
            return MeterLocation.BASEMENT_3
        case "basement4":
            return MeterLocation.BASEMENT_4
        case "basement5":
            return MeterLocation.BASEMENT_5
        case "basement6":
            return MeterLocation.BASEMENT_6
        case "basement7":
            return MeterLocation.BASEMENT_7
        case "basement8":
            return MeterLocation.BASEMENT_8
        case "pit0":
            return MeterLocation.PIT_0
        case "pit1":
            return MeterLocation.PIT_1
        case "pit2":
            return MeterLocation.PIT_2
        case "pit3":
            return MeterLocation.PIT_3
        case "pit4":
            return MeterLocation.PIT_4
        case "pit5":
            return MeterLocation.PIT_5
        case "pit6":
            return MeterLocation.PIT_6
        case "pit7":
            return MeterLocation.PIT_7
        case "pit8":
            return MeterLocation.PIT_8
        case "pit9":
            return MeterLocation.PIT_9
        case _:
            return MeterLocation.UNKNOWN
