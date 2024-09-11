from datetime import datetime
from typing import List, Optional
from models.document import Document
from models.validation_status import ValidationStatus

class HTMLDocument(Document):
    """
    Concrete implementation of Document for HTML files.
    """
    def __init__(
        self,
        document_id: str,
        title: Optional[str],
        header: List[str],
        body: List[List[str]],
        footer: Optional[str],
        country: Optional[str],
        date: Optional[datetime],
        status: ValidationStatus = None
    ):
        super().__init__(document_id, status)
        self.title = title
        self.header = header
        self.body = body
        self.footer = footer
        self.country = country
        self.date = date

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an HTMLDocument instance from a dictionary.
        """
        return cls(
            document_id=data['document_id'],
            title=data.get('title'),
            header=data.get('header', []),
            body=data.get('body', []),
            footer=data.get('footer'),
            country=data.get('country'),
            date=datetime.fromisoformat(data['date']) if data.get('date') else None,
            status=ValidationStatus(data['status']) if data.get('status') else None
        )

    def to_dict(self) -> dict:
        """
        Convert the HTMLDocument instance to a dictionary.
        """
        return {
            'document_id': self.document_id,
            'title': self.title,
            'header': self.header,
            'body': self.body,
            'footer': self.footer,
            'country': self.country,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status.value if self.status else None
        }
