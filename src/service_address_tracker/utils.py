from service_address_tracker.models.asset import Asset
import re
from service_address_tracker.constants import INVALID_VALUES

def parse_inches(value: str) -> float:
    """

    Convert a string like '6"', '2 1/2"', '3 1/4"' into a float (inches).

    Args:
        value (str): the raw string value of the inch length from the file.

    Raises:
        ValueError: if invalid value type is given as an argument.
        ValueError: if the format of the inch increment is not correct.
            (needs to be in whole numbers, fractions, and with an " marking).

    Returns:
        float: the length in inches
    """
    # Remove the double-quote and strip spaces
    s = value.replace('"', '').strip()

    # Match patterns like:
    # - '6'
    # - '2 1/2'
    pattern = r'^\s*(?:(\d+)\s+)?(\d+)?(?:/(\d+))?\s*$'
    match = re.match(pattern, s)

    if not match:
        raise ValueError(f"Invalid format: {value}")

    whole, num, den = match.groups()

    result = 0.0

    # Whole number part
    if whole:
        result += float(whole)
    elif not num and not den:
        # Case: just a whole number like '6'
        return float(s)

    # Fraction part
    if num and den:
        result += float(num) / float(den)

    return result


def address_sort_key(asset: Asset) -> tuple[str, int]:
    """

    Handle function for pandas to sort a dataframe by the
    alphabetical order of street names, then by street numbers.

    Args:
        asset (Asset): the asset to be checked when iterated through
            the handle function.

    Returns:
        tuple[str, int]: the address and order of the asset, respectively.
    """
    address = asset.service_address.strip()

    # Match: number + rest of address
    match = re.match(r"(\d+)\s+(.*)", address)

    if match:
        number = int(match.group(1))
        street_name = match.group(2).strip()
    else:
        # fallback if format is unexpected
        number = 0  # push to end
        street_name = address

    return (street_name, number)