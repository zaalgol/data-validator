from abc import ABC, abstractmethod
from typing import Tuple, Dict
from models.document import Document
from models.validation_status import ValidationStatus

class DocumentValidator(ABC):
    """
    Abstract base class for document validators.
    """
    @abstractmethod
    def validate(self, document: Document) -> Tuple[ValidationStatus, Dict]:
        """
        Abstract method to validate a document.
        Should return a tuple of ValidationStatus and a dictionary of discrepancies.
        """
        pass
