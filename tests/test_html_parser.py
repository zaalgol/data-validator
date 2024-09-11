import unittest
from unittest.mock import patch, mock_open
from parsers.html_parser import HTMLParser
from models.validation_status import ValidationStatus

class TestHTMLParser(unittest.TestCase):
    def setUp(self):
        # Initialize the HTMLParser instance before each test
        self.parser = HTMLParser()

    def test_parse_valid_html(self):
        """
        Test parsing a valid HTML file with all expected elements.
        """
        mock_html_content = '''
        <table id="TestTable">
            <caption>Test Title</caption>
            <thead>
                <tr><th>Header1</th><th>Header2</th></tr>
            </thead>
            <tbody>
                <tr><td>Data1</td><td>Data2</td></tr>
            </tbody>
            <tfoot>
                <tr><td>Creation: 01Jan2020 TestCountry</td></tr>
            </tfoot>
        </table>
        '''
        # Mock the open function to return the mock HTML content
        with patch('builtins.open', mock_open(read_data=mock_html_content)):
            document = self.parser.parse('test_file.html')
            # Assert that the parsed title matches the expected value
            self.assertEqual(document.title, 'Test Title')
            # Assert that the parsed header matches the expected list
            self.assertEqual(document.header, ['Header1', 'Header2'])
            # Assert that the parsed body matches the expected data
            self.assertEqual(document.body, [['Data1', 'Data2']])
            # Assert that the parsed footer matches the expected value
            self.assertEqual(document.footer, 'Creation: 01Jan2020 TestCountry')
            # Assert that the parsed country matches the expected value
            self.assertEqual(document.country, 'TestCountry')
            # Assert that the date was parsed successfully
            self.assertIsNotNone(document.date)
            # Assert that the document status is None (not set)
            self.assertEqual(document.status, None)

    def test_parse_missing_table(self):
        """
        Test parsing an HTML file that does not contain a table element.
        """
        mock_html_content = '<html><body>No table here</body></html>'
        # Mock the open function to return the mock HTML content
        with patch('builtins.open', mock_open(read_data=mock_html_content)):
            document = self.parser.parse('test_file.html')
            # Assert that the document status is set to NOT_PROCESSED due to missing table
            self.assertEqual(document.status, ValidationStatus.NOT_PROCESSED)

    def test_file_not_found(self):
        """
        Test the parser's handling of a FileNotFoundError when the file does not exist.
        """
        # Mock the open function to raise a FileNotFoundError
        with patch('builtins.open', side_effect=FileNotFoundError()):
            document = self.parser.parse('non_existent_file.html')
            # Assert that the document status is set to ERROR due to file not found
            self.assertEqual(document.status, ValidationStatus.ERROR)

if __name__ == '__main__':
    unittest.main()
