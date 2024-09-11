import json
from datetime import datetime
from pathlib import Path
from typing import Dict

class Config:
    """
    Configuration loader class that reads settings from a JSON file.
    """
    def __init__(self, config_file='src/config/config.json'):
        config_path = Path(config_file)
        with config_path.open('r', encoding='utf-8') as f:
            self._config = json.load(f)

        # Convert max_date string to datetime object
        self._config['max_date'] = datetime.strptime(self._config['max_date'], '%Y-%m-%d')

    # Property methods to access configuration settings
    @property
    def mongodb_uri(self) -> str:
        return self._config.get('mongodb_uri')

    @property
    def database_name(self) -> str:
        return self._config.get('database_name')

    @property
    def documents_collection(self) -> str:
        return self._config.get('documents_collection')

    @property
    def min_title_length(self) -> int:
        return self._config.get('min_title_length')

    @property
    def max_date(self) -> datetime:
        return self._config.get('max_date')

    @property
    def max_sum(self) -> float:
        return self._config.get('max_sum')

    @property
    def log_level(self) -> str:
        return self._config.get('log_level')

    @property
    def log_file(self) -> str:
        return self._config.get('log_file')

    @property
    def parser_map(self) -> Dict[str, str]:
        return self._config.get('parser_map', {})

    @property
    def validator_map(self) -> Dict[str, str]:
        return self._config.get('validator_map', {})

    @property
    def document_type_map(self) -> Dict[str, str]:
        return self._config.get('document_type_map', {})

# Instantiate the config object to be used throughout the application
config = Config()
