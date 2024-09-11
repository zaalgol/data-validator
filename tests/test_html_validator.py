import unittest
from validators.html_validator import HTMLValidator
from models.html_document import HTMLDocument
from models.validation_status import ValidationStatus
from datetime import datetime

class TestHTMLValidator(unittest.TestCase):
    def setUp(self):
        # Initialize the HTMLValidator instance before each test
        self.validator = HTMLValidator()

    def test_validate_valid_document(self):
        """
        Test validating a document that meets all validation criteria.
        """
        document = HTMLDocument(
            document_id='doc1',
            title='Valid Document Title',
            header=['Header1', 'Header2'],
            body=[['Company', '100']],
            footer='Footer content',
            country='TestCountry',
            date=datetime(2020, 1, 1),
            status=None
        )
        status, discrepancies = self.validator.validate(document)
        # Assert that the document is valid
        self.assertEqual(status, ValidationStatus.VALID)
        # Assert that no discrepancies were found
        self.assertEqual(discrepancies, {})

    def test_validate_invalid_title(self):
        """
        Test validating a document with a title shorter than the minimum length.
        """
        document = HTMLDocument(
            document_id='doc2',
            title='Short',
            header=['Header1', 'Header2'],
            body=[['Company', '100']],
            footer='Footer content',
            country='TestCountry',
            date=datetime(2020, 1, 1),
            status=None
        )
        status, discrepancies = self.validator.validate(document)
        # Assert that the document is invalid
        self.assertEqual(status, ValidationStatus.INVALID)
        # Assert that a discrepancy for 'title' exists
        self.assertIn('title', discrepancies)

    def test_validate_invalid_date(self):
        """
        Test validating a document with a date beyond the maximum allowed date.
        """
        document = HTMLDocument(
            document_id='doc3',
            title='Valid Document Title',
            header=['Header1', 'Header2'],
            body=[['Company', '100']],
            footer='Footer content',
            country='TestCountry',
            date=datetime(2023, 1, 1),  # Date beyond max_date in config
            status=None
        )
        status, discrepancies = self.validator.validate(document)
        # Assert that the document is invalid
        self.assertEqual(status, ValidationStatus.INVALID)
        # Assert that a discrepancy for 'date' exists
        self.assertIn('date', discrepancies)

    def test_validate_sum_exceeds_max(self):
        """
        Test validating a document where the sum of the first row exceeds the maximum allowed sum.
        """
        document = HTMLDocument(
            document_id='doc4',
            title='Valid Document Title',
            header=['Header1', 'Header2'],
            body=[['Company', '6000']],  # Sum exceeds max_sum in config
            footer='Footer content',
            country='TestCountry',
            date=datetime(2020, 1, 1),
            status=None
        )
        status, discrepancies = self.validator.validate(document)
        # Assert that the document is invalid
        self.assertEqual(status, ValidationStatus.INVALID)
        # Assert that a discrepancy for 'first_row' exists
        self.assertIn('first_row', discrepancies)

if __name__ == '__main__':
    unittest.main()
