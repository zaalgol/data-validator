from typing import Tuple, Dict
from models.html_document import HTMLDocument
from models.validation_status import ValidationStatus
from config.config_loader import config
from utils.logger import get_logger

logger = get_logger(__name__)

class HTMLValidator:
    """
    Validator for HTML documents.
    """
    def validate(self, document: HTMLDocument) -> Tuple[ValidationStatus, Dict]:
        """
        Validate an HTML document and return its validation status and discrepancies.
        """
        if document.status in [ValidationStatus.ERROR, ValidationStatus.NOT_PROCESSED]:
            return document.status, {}

        discrepancies = {}

        # Validate title
        if not document.title:
            discrepancies['title'] = {
                'type': 'missing_value',
                'details': 'Missing title'
            }
        elif len(document.title) < config.min_title_length:
            discrepancies['title'] = {
                'type': 'wrong_value',
                'details': f"Title is shorter than {config.min_title_length} characters"
            }

        # Validate date
        if not document.date:
            discrepancies['date'] = {
                'type': 'missing_value',
                'details': 'Missing or invalid date'
            }
        elif document.date > config.max_date:
            discrepancies['date'] = {
                'type': 'wrong_value',
                'details': f"Date {document.date.date()} is beyond {config.max_date.date()}"
            }

        # Validate sum of first row
        try:
            first_row_values = document.body[0][1:]
            first_row_sum = sum(
                float(value.rstrip('%')) for value in first_row_values if value.rstrip('%').replace('.', '', 1).isdigit()
            )
            if first_row_sum > config.max_sum:
                discrepancies['first_row'] = {
                    'type': 'wrong_value',
                    'details': f"Sum of first row ({first_row_sum}) is higher than {config.max_sum}"
                }
        except (IndexError, ValueError) as e:
            logger.warning(f"Error calculating sum of first row in document {document.document_id}: {e}")
            discrepancies['first_row'] = {
                'type': 'calculation_error',
                'details': 'Error calculating sum of first row'
            }

        if discrepancies:
            return ValidationStatus.INVALID, discrepancies
        return ValidationStatus.VALID, {}
