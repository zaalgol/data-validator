import importlib

class Factory:
    """
    Factory class for creating parsers, validators, and document instances.
    Caches instances to prevent unnecessary re-instantiation.
    """
    _parser_instances = {}
    _validator_instances = {}

    @staticmethod
    def create_instance(class_path: str):
        """
        Dynamically create an instance of a class given its full module path.
        """
        try:
            module_name, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            return cls()
        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Cannot create instance of {class_path}: {e}")

    @staticmethod
    def create_parser(parser_class_path: str):
        """
        Create or retrieve a cached parser instance.
        """
        if parser_class_path not in Factory._parser_instances:
            Factory._parser_instances[parser_class_path] = Factory.create_instance(parser_class_path)
        return Factory._parser_instances[parser_class_path]

    @staticmethod
    def create_validator(validator_class_path: str):
        """
        Create or retrieve a cached validator instance.
        """
        if validator_class_path not in Factory._validator_instances:
            Factory._validator_instances[validator_class_path] = Factory.create_instance(validator_class_path)
        return Factory._validator_instances[validator_class_path]

    @staticmethod
    def create_document(document_class_path: str, data):
        """
        Create a document instance from a dictionary of data.
        """
        try:
            module_name, class_name = document_class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            return cls.from_dict(data)
        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Cannot create document of type {document_class_path}: {e}")
