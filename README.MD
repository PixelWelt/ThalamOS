# ThalamOS
![Build Status](https://img.shields.io/github/workflow/status/PixelWelt/ThalamOS/docker.yml)
![License](https://img.shields.io/github/license/PixelWelt/ThalamOS)
![Issues](https://img.shields.io/github/issues/PixelWelt/ThalamOS)
![Forks](https://img.shields.io/github/forks/PixelWelt/ThalamOS)
![Stars](https://img.shields.io/github/stars/PixelWelt/ThalamOS)
![Commits since latest release](https://img.shields.io/github/commits-since/PixelWelt/ThalamOS/latest)
![Contributors](https://img.shields.io/github/contributors/PixelWelt/ThalamOS)
![created at](https://img.shields.io/github/created-at/PixelWelt/ThalamOS)
![last commit](https://img.shields.io/github/last-commit/PixelWelt/ThalamOS)
Thalamos is a powerful Flask web application designed to enhance your storage management. It utilizes the WLED-API to light up the item you are looking for.
## Features

- **LED Integration**: Controls an addressable LED strip via WLED to highlight the correct location of your items.
- **Custom Properties**: Save any property with your stored items using the info field, allowing for infinite key-value pairs.
- **Search Functionality**: Easily search for items and see their location light up on your storage shelf.
- **Lightweight**: Built with SQLite and Flask, ensuring minimal resource usage and easy deployment.
- **Easy Deployment**: Deploy effortlessly using a Docker container.

## Installation
### build-it-yourself
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/thalamos.git
    ```
2. Navigate to the project directory:
    ```bash
    cd thalamos/app
    ```
3. Build the container:
    ```bash
    docker build -t PixelWelt/thalamos .
    ```
4. insert your WLED_HOST into the .env.example file and rename it to .env
5. Run the application using the docker compose file:
    ```bash
    cd ..
    docker-compose up
    ```

## Usage

1. Open your web browser and go to `http://localhost:8000`.
2. Add your stored items along with their properties.
3. Use the search functionality to find items and see their location light up on your storage shelf.

## Images
![home page](img/home-page.png)
![create Item page](img/createItem.png)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.