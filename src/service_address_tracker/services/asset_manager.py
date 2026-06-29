# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:27:04 2026

@author: c10265
"""


from service_address_tracker.models.asset import Asset
from service_address_tracker.utils import parse_inches
import pandas as pd


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
    df["Public Diameter"] = df["Public Diameter"].fillna(-1)
    

    # Removes duplicate service addresses. Does not account for duplicate
    # owner names or contact information on related, but not exact,
    # service addresses.
    records = df.to_dict("records")
    print(records)

    assets = []

    """ for r in records:
        try:
            asset = Asset(
                object_id=int(r.get("OBJECTID")),
                service_address=str(r.get("Service Address")),
                project_number=str(r.get("Project Number")),
                project_category=str(r.get(
                    "Type of Service Replacement (Project Category)"
                )),
                property_owner_name=str(r.get("Property Owner Name")),
                property_owner_phone_number=str(r.get(
                    "Property Owner Phone Number"
                )),
                property_owner_phone_number_additional=str(r.get(
                    "Additional Property Owner Phone"
                )),
                property_owner_email=str(r.get("Property Owner Email")),
                property_owner_address=str(r.get("Property Owner Address")),
                property_owner_city_state_zip=str(r.get("City,State,ZIP")),
                primary_tenant_name=str(r.get("Primary Tenant Name")),
                primary_tenant_phone_number=str(r.get(
                    "Primary Tenant Phone Number"
                )),
                primary_tenant_email=str(r.get("Primary Tenant Email")),
                public_diameter=parse_inches(r.get("Public Diameter")),
                zip_code=int(r.get("Zip Code")),
                private_property_access=str(r.get("Private Property Access")),
                grantor_access_name_construction=str(r.get(
                    "Grantor Access Name Construction"
                )),
                grantor_access_name_preconstruction=str(r.get(
                    "Grantor Access Name Preconstruction"
                )),
                decliner_name=str(r.get("Name of Decliner")),
                status=Status.TO_CONTACT
            )
            assets.append(asset)
        except Exception as e:
            raise e """

    return assets
