# Minimum version of CMake required
cmake_minimum_required(VERSION 3.12)

# Project name
project(visioncraft)

# --- Find Python ---
# This tells CMake to find the Python interpreter, libraries, and include directories.
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# --- Find OpenCV ---
# This finds the OpenCV library. It's required for our C++ code.
find_package(OpenCV REQUIRED)
# Include the OpenCV directories
include_directories(${OpenCV_INCLUDE_DIRS})

# --- Find pybind11 ---
# This finds the pybind11 library, which we use to create the Python bindings.
find_package(pybind11 CONFIG REQUIRED)

# --- Define the C++ Target ---
# pybind11_add_module is a special function from pybind11.
# It creates a Python module from our C++ source file.
#
# ARGUMENTS:
# 1. visioncraft_cpp: The name of the Python module we are creating.
# 2. image_processor.cpp: The C++ source file to compile.
pybind11_add_module(visioncraft_cpp image_processor.cpp)

# --- Link Libraries ---
# We need to link our module against the OpenCV libraries.
# ${OpenCV_LIBS} contains the list of all necessary OpenCV library files.
target_link_libraries(visioncraft_cpp PRIVATE ${OpenCV_LIBS})

# Set C++ standard to C++17
set_target_properties(visioncraft_cpp PROPERTIES CXX_STANDARD 17)

