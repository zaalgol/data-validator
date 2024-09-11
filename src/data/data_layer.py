from pymongo import MongoClient
from typing import Dict, Optional

class DataLayer:
    """
    Data access layer for interacting with the MongoDB database.
    """
    def __init__(self, config):
        # Initialize MongoDB client and select the database and collection
        self.client = MongoClient(config.mongodb_uri)
        self.db = self.client[config.database_name]
        self.documents = self.db[config.documents_collection]

    def upsert_document(self, document: Dict):
        """
        Insert or update a document in the database.
        """
        self.documents.update_one(
            {'document_id': document['document_id']},
            {'$set': document},
            upsert=True
        )

    def update_document(self, document_id: str, update_data: Dict) -> None:
        """
        Update fields of an existing document in the database.
        """
        self.documents.update_one({'document_id': document_id}, {'$set': update_data})

    def get_document(self, document_id: str) -> Optional[Dict]:
        """
        Retrieve a document from the database by its document ID.
        """
        return self.documents.find_one({'document_id': document_id})

    def delete_document(self, document_id: str) -> None:
        """
        Delete a document from the database by its document ID.
        """
        self.documents.delete_one({'document_id': document_id})
