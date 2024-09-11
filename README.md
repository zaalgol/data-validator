# Document Processing and Validation System

## Project Description

This project is a document processing and validation system designed to parse HTML documents, extract relevant information, store the data in a MongoDB database, and validate the documents based on specific criteria. The system is modular, extensible for adding other file types and validators, and utilizes design patterns to promote maintainability and scalability.

## Project Structure

The project is organized into the following main components:

- **`src/`**: The source code directory containing all modules.
  - **`main.py`**: The entry point of the application.
  - **`config/`**: Configuration files and loaders.
  - **`data/`**: Data access layer for database interactions.
  - **`factory/`**: Factory classes for object creation.
  - **`models/`**: Data models and enums.
  - **`parsers/`**: Parsers for different document types.
  - **`services/`**: Service layer orchestrating parsing and validation.
  - **`utils/`**: Utility functions such as logging.
  - **`validators/`**: Validators for documents.
- **`documents/`**: Directory containing sample HTML documents to be processed.
- **`tests/`**: Unit tests for the application components.
- **`requirements.txt`**: Python dependencies.

## How to Run the Project

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up MongoDB**:

   Ensure that MongoDB is installed and running on your local machine or update the mongodb_uri in src/config/config.json to point to your MongoDB instance.

3. **Set Up MongoDB**:
   ```bash
   python src/main.py
   ```

## How to Run the Tests
   ```bash
   pytest tests/
   ```

## Design Patterns Used

### Factory Pattern

The Factory Pattern is used to create instances of parsers, validators, and documents without specifying the exact class. This is particularly useful when the types of objects to be created are determined at runtime.

* **Implementation:** The Factory class in `src/factory/factory.py` creates instances based on configuration mappings defined in `src/config/config.json`.
* **Pros:** Decouples object creation, promotes extensibility, centralizes object management.
* **Cons:** Increased complexity, potential for runtime errors.

### Dependency Injection

Dependency Injection is used to inject dependencies into classes rather than having them instantiate dependencies internally.

* **Implementation:** Evident in classes like DocumentService where parsers and data layers are injected.
* **Pros:** Enhances testability, increases flexibility, reduces coupling.
* **Cons:** Requires careful management, potential for over-engineering.

### Singleton Pattern (Avoided)

The Singleton Pattern was consciously avoided in favor of instance caching within the Factory class.

* **Reasons for Avoiding:** Introduces global state, difficulties in testing, flexibility constraints.
* **Instance Caching Benefits:** Controlled reuse, enhanced testability.

### Separation of Concerns

The principle of Separation of Concerns is heavily utilized, separating functionality into distinct layers and modules.

* **Benefits:** Improved maintainability, enhanced readability, facilitated collaboration.

## Overall Design Considerations

The combination of these design patterns and principles results in a system that is:

* **Modular:** Components can be developed, tested, and maintained independently.
* **Extensible:** New document types, parsers, or validators can be added easily.
* **Testable:** Loose coupling and dependency injection make unit testing straightforward.
* **Maintainable:** Clear separation of concerns and centralized configuration simplify maintenance. 