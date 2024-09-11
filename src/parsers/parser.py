import os
from typing import List
from models.document import Document
from models.validation_status import ValidationStatus
from config.config_loader import config
from factory.factory import Factory
from utils.logger import get_logger

logger = get_logger(__name__)

class Parser:
    """
    General parser that delegates to specific parsers based on file extension.
    """
    def parse(self, folder_path: str) -> List[Document]:
        """
        Parse all files in a given folder.
        """
        parsed_documents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                continue
            file_extension = os.path.splitext(filename)[1][1:].lower()
            parser_class_path = config.parser_map.get(file_extension, config.parser_map['default'])
            specific_parser = Factory.create_parser(parser_class_path)

            try:
                document = specific_parser.parse(file_path)
                parsed_documents.append(document)
                logger.info(f"Document {filename} parsed successfully.")
            except Exception as e:
                logger.exception(f"Error parsing document {filename}: {e}")
                parsed_documents.append(Document(filename, ValidationStatus.ERROR))

        return parsed_documents
