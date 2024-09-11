import unittest
from unittest.mock import MagicMock, patch
from services.document_service import DocumentService
from models.validation_status import ValidationStatus

class TestDocumentService(unittest.TestCase):
    @patch('services.document_service.Parser')
    @patch('services.document_service.DataLayer')
    def test_parse_documents(self, mock_data_layer_class, mock_parser_class):
        """
        Test the parse_documents method of DocumentService.
        """
        # Mock the Parser and DataLayer classes
        mock_parser = mock_parser_class.return_value
        mock_data_layer = mock_data_layer_class.return_value

        # Create a mock document with necessary attributes
        document = MagicMock()
        document.document_id = 'doc1'
        document.status = None
        document.to_dict.return_value = {'document_id': 'doc1'}

        # Mock the parse method to return a list containing the mock document
        mock_parser.parse.return_value = [document]

        # Initialize the DocumentService with mocked dependencies
        service = DocumentService(data_layer=mock_data_layer, parser=mock_parser)
        document_ids = service.parse_documents('dummy_folder')

        # Assert that the document ID is returned
        self.assertEqual(document_ids, ['doc1'])
        # Assert that upsert_document was called with the correct arguments
        mock_data_layer.upsert_document.assert_called_with({'document_id': 'doc1'})

    @patch('services.document_service.Factory')
    @patch('services.document_service.DataLayer')
    def test_validate_documents(self, mock_data_layer_class, mock_factory_class):
        """
        Test the validate_documents method of DocumentService.
        """
        # Mock the DataLayer class
        mock_data_layer = mock_data_layer_class.return_value
        # Mock get_document to return a sample document data
        mock_data_layer.get_document.return_value = {'document_id': 'doc1', 'status': 'VALID'}

        # Mock the validator to return VALID status with no discrepancies
        mock_validator = MagicMock()
        mock_validator.validate.return_value = (ValidationStatus.VALID, {})
        mock_factory_class.create_validator.return_value = mock_validator

        # Mock the creation of a document instance
        mock_factory_class.create_document.return_value = MagicMock()

        # Initialize the DocumentService with mocked dependencies
        service = DocumentService(data_layer=mock_data_layer)
        service.validate_documents(['doc1'])

        # Assert that update_document was called with the correct arguments
        mock_data_layer.update_document.assert_called_with('doc1', {'discrepancies': {}, 'status': 'VALID'})

if __name__ == '__main__':
    unittest.main()
