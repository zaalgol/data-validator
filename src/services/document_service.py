import os
from typing import List
from data.data_layer import DataLayer
from parsers.parser import Parser
from models.validation_status import ValidationStatus
from factory.factory import Factory
from config.config_loader import config
from utils.logger import get_logger

logger = get_logger(__name__)

class DocumentService:
    """
    Service layer that orchestrates parsing and validation of documents.
    """
    def __init__(self, data_layer=None, parser=None):
        self.data_layer = data_layer or DataLayer(config)
        self.parser = parser or Parser()

    def parse_documents(self, folder_path: str) -> List[str]:
        """
        Parse documents in a folder and store them in the database.
        Returns a list of document IDs.
        """
        parsed_documents = self.parser.parse(folder_path)
        document_ids = []

        for document in parsed_documents:
            document_ids.append(document.document_id)

            if document.status in [ValidationStatus.ERROR, ValidationStatus.NOT_PROCESSED]:
                # Store only the status if parsing failed
                self.data_layer.upsert_document({
                    'document_id': document.document_id,
                    'status': document.status.value
                })
                logger.info(f"Document {document.document_id} - Status: {document.status.value}")
            else:
                # Store the full document data
                doc_dict = document.to_dict()
                self.data_layer.upsert_document(doc_dict)
                logger.info(f"Document {document.document_id} content stored.")

        return document_ids

    def validate_documents(self, document_ids: List[str]):
        """
        Validate documents based on their IDs and update their status and discrepancies.
        """
        for doc_id in document_ids:
            doc_data = self.data_layer.get_document(doc_id)
            if not doc_data:
                logger.warning(f"Document {doc_id} not found in database")
                continue

            file_extension = os.path.splitext(doc_data['document_id'])[1][1:].lower()
            validator_class_path = config.validator_map.get(file_extension, config.validator_map['default'])
            validator = Factory.create_validator(validator_class_path)
            document_class_path = config.document_type_map.get(file_extension, config.document_type_map['default'])

            try:
                document = Factory.create_document(document_class_path, doc_data)
                status, discrepancies = validator.validate(document)
                update_dict = {
                    'discrepancies': discrepancies,
                    'status': status.value
                }
                self.data_layer.update_document(doc_id, update_dict)
                logger.info(f"Document {doc_id} validated. Status: {status.value}")
            except Exception as e:
                logger.exception(f"Error validating document {doc_id}: {e}")
                self.data_layer.update_document(doc_id, {'status': ValidationStatus.ERROR.value})
