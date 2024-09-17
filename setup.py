# setup.py
from setuptools import setup
import os

APP = ['realesrgan_gui.py']  # Main application file
DATA_FILES = [
    ('assets', 'assets'),  # Ensures assets folder is included
    ('realesrgan', 'realesrgan'),  # Include the entire realesrgan folder
    ('realesrgan/models', 'realesrgan/models'),  # Include the models folder
]
OPTIONS = {
    'argv_emulation': True,
    'packages': [],
    'excludes': [],
    'iconfile': 'assets/magic-wand.ico',  # Path to your icon file
}

# Include the Real-ESRGAN executable
binaries = [
    ('realesrgan/realesrgan-ncnn-vulkan.exe', 'realesrgan'),  # Path for Windows executable
]

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    binaries=binaries,
)
