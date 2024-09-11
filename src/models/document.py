from abc import ABC, abstractmethod
from models.validation_status import ValidationStatus

class Document(ABC):
    """
    Abstract base class for documents.
    """
    def __init__(self, document_id: str, status: ValidationStatus = None):
        self.document_id = document_id
        self.status = status

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """
        Abstract method to create a document instance from a dictionary.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Abstract method to convert the document instance to a dictionary.
        """
        pass
