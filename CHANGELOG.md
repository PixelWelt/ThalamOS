# Changelog

## 0.2.3 - 2025-10-25
### Cleanup
* Migrated to uv
* updated unsecure dependencies
* cleaned up README
* added Changelog file for better tracking of changes
* updated Versions to use semantic versioning

## 0.2.2 - 2025-04-16
### Security patch
* updated Cryptography pacakge

## 0.2.1 - 2025-04-02
## Security patch
* updated Cryptography pacakge
* updated jinja2 to remove vulnerability

## 0.2.0 - 2025-02-11
## Modules und QOL Updates
This version introduces two major optional modules: the Ollama-based AI Assistant and Weigh-Fi functionality. These new features are designed to significantly enhance your experience with ThalamOS. It also introduces some other quality of life features.

### Features:
* Added Ollama-based AI Assistant
* Implemented Weigh-Fi functionality
* Added function to allow users to update item details during review
* Added German translation for README
* Enabled multiplatform build
* Added centralized logging using Loguru
* Added logging endpoint for frontend
* Enhanced UI
* Updated documentation
* Improved .env file configuration
* Migrated to pyproject.toml
* Enhanced code readability with variable annotations
### Other Changes:
* Added favicon

## 0.1.0 - 2025-01-04
### Initial Release
The first release of ThalamOS is here, a powerful Flask web application designed to enhance your storage management. ThalamOS utilizes the WLED-API to light up the item you are looking for, making it easier to find and organize your stored items.
### Features:
* LED Integration: Controls an addressable LED strip via WLED to highlight the correct location of your items.
* Custom Properties: Save any property with your stored items using the info field, allowing for infinite key-value pairs.
* Search Functionality: Easily search for items and see their location light up on your storage shelf.
* Lightweight: Built with SQLite and Flask, ensuring minimal resource usage and easy deployment.
* Easy Deployment: Deploy effortlessly using a Docker container.