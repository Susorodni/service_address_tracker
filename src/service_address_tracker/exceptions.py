"""

This module contains exceptions used in the service address tracker application.

"""
class AssetNotFoundException(Exception):
    pass

class InvalidDataImportException(Exception):
    pass

class NoFlagApplicationException(Exception):
    """Raised when no flag category could be applied.

    Args:
        Exception (Exception): base Exception
    """
    def __init__(self, service_address: str, message: str | None = None):
        self.service_address = service_address
        
        if message is None:
            message = (
                f"No flag category could be applied to service address {self.service_address}."
            )
            
        super().__init__(message)