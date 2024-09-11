from enum import Enum

class ValidationStatus(Enum):
    """
    Enumeration of possible validation statuses for a document.
    """
    VALID = 'VALID'
    INVALID = 'INVALID'
    ERROR = 'ERROR'
    NOT_PROCESSED = 'NOT_PROCESSED'
