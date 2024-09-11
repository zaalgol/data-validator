from dataclasses import dataclass

@dataclass
class Discrepancy:
    """
    Data class representing a discrepancy found during validation.
    """
    field: str
    type: str
    details: str

    def to_dict(self):
        """
        Convert the Discrepancy instance to a dictionary.
        """
        return {
            'field': self.field,
            'type': self.type,
            'details': self.details
        }
