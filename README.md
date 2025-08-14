# VisionCraft  
**A Cross-Language Image Processing Tool**

VisionCraft is a **lightweight yet powerful image-processing application** that demonstrates the synergy between **C++** and **Python**.  
It leverages the **high performance of C++ with OpenCV** for rapid image filtering and combines it with a **user-friendly GUI** built in Python with Tkinter.

The core idea is simple:  
- **C++** handles all computationally intensive tasks (blur, sharpen, edge detection, etc.)  
- **Python** manages the user interface and application logic  
- The two communicate seamlessly via **Pybind11** bindings  

---

## ✨ Key Features
- **High-Performance Backend** – All image processing is executed in C++ for maximum speed.  
- **Image Rotation** – Rotate images 90° left or right instantly.  
- **Interactive Cropping** – Click and drag to select a region, then crop with one button press.  
- **Core Filters**:  
  - Grayscale Conversion  
  - Gaussian Blur  
  - Canny Edge Detection  
  - Image Sharpening  
- **Load & Save** – Open and save images in `.png`, `.jpg`, `.bmp` formats.  

---

## 🛠 Tech Stack
| Component              | Technology |
|------------------------|------------|
| Backend                | C++17 + OpenCV |
| Frontend / GUI         | Python 3.10+ + Tkinter |
| C++/Python Bridge      | Pybind11 |
| Build System           | CMake |

---

## 📂 Project Structure

visioncraft/ <br />
├── build/                       
├── image_processor.cpp     <br />
├── gui.py                  <br />
└── CMakeLists.txt          <br />


---

## 🚀 Setup & Usage (Ubuntu/Debian)
Follow these steps to install and run VisionCraft locally.

### 1️⃣ Install Prerequisites
```bash
# Update package list
sudo apt update

# Install compiler & build tools
sudo apt install -y g++ cmake build-essential

# Install Python & Tkinter
sudo apt install -y python3-dev python3-pip python3-tk

# Pillow for image display in Tkinter
sudo apt install -y python3-pil.imagetk

# Python libraries
pip3 install opencv-python-headless numpy

# OpenCV development library for C++
sudo apt install -y libopencv-dev

# Pybind11 for C++/Python bindings
sudo apt install -y pybind11-dev

```
### 2️⃣ Build the C++ Module
```bash
# Navigate to the project directory
cd fastvision/

# Create a build directory if it doesn't exist
mkdir -p build
cd build

# Run CMake to generate the build files
cmake ..

# Run make to compile the C++ code
make

```

If the build is successful, a new file named visioncraft_cpp.cpython-*.so will be created or updated inside the build directory.   <br />
Move visioncraft_cpp.cpython-*.so to where the file gui.py is located   <br />
Run gui.py file
