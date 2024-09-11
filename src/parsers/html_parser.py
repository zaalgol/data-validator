from typing import Any, Optional
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from models.html_document import HTMLDocument
from models.validation_status import ValidationStatus
from utils.logger import get_logger

logger = get_logger(__name__)

class HTMLParser:
    """
    Parser for HTML documents.
    """
    def parse(self, file_path: str) -> HTMLDocument:
        """
        Parse an HTML file and extract document information.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return self._parse_content(content, file_path)
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return HTMLDocument(file_path, None, [], [], None, None, None, ValidationStatus.ERROR)
        except Exception as e:
            logger.exception(f"An error occurred while parsing {file_path}: {e}")
            return HTMLDocument(file_path, None, [], [], None, None, None, ValidationStatus.ERROR)

    def _parse_content(self, content: str, file_path: str) -> HTMLDocument:
        """
        Internal method to parse the content of an HTML file.
        """
        soup = BeautifulSoup(content, 'html.parser')

        # Extract the title from the caption element
        title_element = soup.find('caption')
        title = title_element.text.strip() if title_element else None

        # Find the table in the HTML
        table = soup.find('table')
        if not table:
            logger.warning(f"No table found in {file_path}")
            return HTMLDocument(file_path, title, None, None, None, None, None, ValidationStatus.NOT_PROCESSED)

        # Extract headers from the table
        header = [th.text.strip() for th in table.find_all('th')]

        # Extract body rows from the table
        tbody = table.find('tbody')
        if tbody:
            body_rows = tbody.find_all('tr')
        else:
            body_rows = table.find_all('tr')[1:-1]  # Exclude header and footer
        body = [[td.text.strip() for td in tr.find_all('td')] for tr in body_rows]

        # Parse the footer to extract date and country
        footer, date, country = self._parse_footer(table, file_path)

        return HTMLDocument(file_path, title, header, body, footer, country, date, None)

    def _parse_footer(self, table, file_path) -> tuple[Optional[str], Optional[Any], Optional[str]]:
        """
        Parse the footer of the table to extract creation date and country.
        """
        footer = None
        date = None
        country = None

        footer_element = table.find('tfoot')
        if not footer_element:
            logger.warning(f"No tfoot element in {file_path}")
        else:
            footer_row = footer_element.find('tr')
            footer_cell = footer_row.find('td')
            footer = footer_cell.text.strip()

            if footer:
                footer_text = footer.replace('Creation:', '').strip()
                try:
                    # Split footer text to separate date and country
                    footer_parts = footer_text.split(' ', 1)
                    date_str = footer_parts[0]
                    country = footer_parts[1] if len(footer_parts) > 1 else None
                    try:
                        date = date_parser.parse(date_str, fuzzy=True)
                    except Exception:
                        # If date parsing fails, assume entire footer is country
                        country = footer_text
                except ValueError as e:
                    logger.warning(f"Failed to parse date and country from footer in {file_path}: {e}")
        return footer, date, country
