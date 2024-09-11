from services.document_service import DocumentService
from utils.logger import get_logger

# Initialize the logger for this module
logger = get_logger(__name__)

def main():
    """
    Main function to orchestrate the parsing and validation of documents.
    """
    document_service = DocumentService()
    folder_path = 'documents/'

    # Stage 1: Parsing and storing documents
    logger.info("Starting Stage 1: Parsing and storing documents")
    document_ids = document_service.parse_documents(folder_path)
    logger.info(f"Processed {len(document_ids)} documents")

    # Stage 2: Validating documents
    logger.info("Starting Stage 2: Validating documents")
    document_service.validate_documents(document_ids)

if __name__ == "__main__":
    main()
