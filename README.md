# VisionCraft

VisionCraft – A Cross-Language Image Processing Tool
VisionCraft is a lightweight but powerful image-processing application that demonstrates the synergy between C++ and Python. It leverages the high performance of C++ with OpenCV for rapid image filtering and combines it with a user-friendly GUI built in Python with Tkinter.

The core principle is to delegate all computationally intensive tasks (like blur, sharpen, edge detection) to a compiled C++ backend, while Python handles the user interface and application logic. The two languages communicate seamlessly through bindings created with pybind11.

✨ Key Features
High-Performance Backend: All image processing is done in C++ for maximum speed.

Image Rotation: Easily rotate images 90 degrees left or right.

Interactive Cropping: Click and drag on the image to select a region, then crop with a single button press.

Core Image Filters:

Grayscale Conversion

Gaussian Blur

Canny Edge Detection

Image Sharpening

Load & Save: Easily open and save images in common formats (.png, .jpg, .bmp).

🛠️ Tech Stack
Backend: C++17

Frontend/GUI: Python 3.10+

Image Processing: OpenCV

C++/Python Bridge: Pybind11

Build System: CMake

📂 Project Structure
fastvision/
├── build/                  # Created during the build process
├── image_processor.cpp     # C++ source for all image filters
├── gui.py                  # Python source for the Tkinter UI
└── CMakeLists.txt          # Build script for CMake

🚀 Setup and Usage (for Ubuntu/Debian-based Linux)
Follow these steps to get the application running on your local machine.

1. Prerequisites
First, install all the required tools and libraries. Open your terminal and run:

# Update package list
sudo apt update

# Install C++ compiler, CMake, and build tools
sudo apt install -y g++ cmake build-essential

# Install Python, Pip, and Tkinter
sudo apt install -y python3-dev python3-pip python3-tk

# Install the Pillow library with Tkinter support
sudo apt install -y python3-pil.imagetk

# Install Python libraries (OpenCV for reading/writing images)
pip3 install opencv-python-headless numpy

# Install the main OpenCV development library for C++
sudo apt install -y libopencv-dev

# Install pybind11 for C++/Python bindings
sudo apt install -y pybind11-dev

2. Build the C++ Module
Any time you change the C++ code, you must re-compile it.

# Navigate to the project directory
cd visioncraft/

# Create a build directory if it doesn't exist
mkdir -p build
cd build

# Run CMake to generate the build files
cmake ..

# Run make to compile the C++ code
make

If the build is successful, a new file named visioncraft_cpp.cpython-*.so will be created or updated inside the build directory.
Move visioncraft_cpp.cpython-*.so to where the file gui.py is located
Run gui.py file
