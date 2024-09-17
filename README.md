# Real-ESRGAN Image Processor

## Overview

The **Real-ESRGAN Image Processor** is a user-friendly application for enhancing images using the Real-ESRGAN model. It allows you to load images, process them with high-quality upscaling, and save the enhanced results. The application features a clean and intuitive graphical user interface (GUI) built with Python's Tkinter library.

![Application Screenshot](assets/screenshot.png)

## Features

- **Load Images**: Select images from your file system for processing.
- **Process Images**: Enhance images using the Real-ESRGAN model.
- **Save Output**: Choose the location to save the processed image.
- **Progress Tracking**: Monitor the progress of image processing.
- **Dark Mode**: Toggle between light and dark mode for a better visual experience.

## Installation

To get started, you'll need Python 3.12 or later installed on your system. Follow these steps to set up the application:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/PhotoEditor.git
    cd PhotoEditor
    ```

2. **Install Dependencies**:
    Ensure you have the required Python libraries. You can install them using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. **Build the Application**:
    - For Windows:
        ```bash
        python setup.py py2exe
        ```
    - For macOS:
        ```bash
        python setup.py py2app
        ```

4. **Run the Application**:
    - On Windows, navigate to the `dist` folder and run `PhotoEditor.exe`.
    - On macOS, navigate to the `dist` folder and open `PhotoEditor.app`.

## Contributing

The Real-ESRGAN Image Processor is an open-source project created by **Whitelightning Dev**. We welcome contributions and improvements! If you'd like to contribute, please follow these guidelines:

1. **Fork the Repository**: Create a personal copy of the project by forking it on GitHub.
2. **Create a Branch**: Develop your changes in a new branch.
3. **Submit a Pull Request**: Once your changes are ready, submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or feedback, please reach out to Whitelightning Dev at [danielmommsen@hotmail.com].
