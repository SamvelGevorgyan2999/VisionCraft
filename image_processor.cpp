#include <opencv4/opencv2/opencv_modules.hpp>
#include <opencv4/opencv2/opencv.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// Helper function to convert cv::Mat to a Python numpy array.
// This allows us to send image data back to Python.
py::array_t<unsigned char> mat_to_nparray(const cv::Mat& img) {
    cv::Mat continuous_img;
    if (!img.isContinuous()) {
        img.copyTo(continuous_img);
    } else {
        continuous_img = img;
    }

    std::vector<ssize_t> shape;
    if (continuous_img.channels() == 1) {
        shape = { (ssize_t)continuous_img.rows, (ssize_t)continuous_img.cols };
    } else {
        shape = { (ssize_t)continuous_img.rows, (ssize_t)continuous_img.cols, (ssize_t)continuous_img.channels() };
    }

    std::vector<ssize_t> strides;
     if (continuous_img.channels() == 1) {
        strides = { (ssize_t)continuous_img.cols * sizeof(unsigned char), sizeof(unsigned char) };
    } else {
        strides = { (ssize_t)continuous_img.cols * continuous_img.channels() * sizeof(unsigned char), (ssize_t)continuous_img.channels() * sizeof(unsigned char), sizeof(unsigned char) };
    }

    return py::array_t<unsigned char>(
        shape,
        strides,
        continuous_img.data
    );
}

// Helper function to convert a Python numpy array to a cv::Mat.
cv::Mat nparray_to_mat(py::array_t<unsigned char>& arr) {
    py::buffer_info info = arr.request();

    int cv_type = 0;
    if (info.ndim == 3) {
        cv_type = CV_8UC3;
    } else if (info.ndim == 2) {
        cv_type = CV_8UC1;
    } else {
        throw std::runtime_error("Input numpy array must be 2 or 3-dimensional");
    }

    return cv::Mat(info.shape[0], info.shape[1], cv_type, (unsigned char*)info.ptr);
}

// C++ function to convert an image to grayscale.
cv::Mat to_grayscale(const cv::Mat& input_image) {
    cv::Mat gray_image;
    cv::cvtColor(input_image, gray_image, cv::COLOR_BGR2GRAY);
    return gray_image;
}

// C++ function to apply a Gaussian blur.
cv::Mat apply_blur(const cv::Mat& input_image) {
    cv::Mat blurred_image;
    cv::GaussianBlur(input_image, blurred_image, cv::Size(15, 15), 0);
    return blurred_image;
}

// C++ function for Canny edge detection.
cv::Mat detect_edges(const cv::Mat& input_image) {
    cv::Mat gray_image, edges;
    cv::cvtColor(input_image, gray_image, cv::COLOR_BGR2GRAY);
    cv::Canny(gray_image, edges, 100, 200);
    return edges;
}

// C++ function to sharpen an image.
cv::Mat sharpen_image(const cv::Mat& input_image) {
    cv::Mat sharpened_image;
    cv::Mat kernel = (cv::Mat_<float>(3, 3) <<
        0, -1,  0,
       -1,  5, -1,
        0, -1,  0);
    cv::filter2D(input_image, sharpened_image, -1, kernel);
    return sharpened_image;
}

// C++ function to crop an image given a rectangle.
cv::Mat crop_image(const cv::Mat& input_image, int x, int y, int width, int height) {
    cv::Rect roi(x, y, width, height);
    cv::Rect img_bounds(0, 0, input_image.cols, input_image.rows);
    roi = roi & img_bounds;

    if (roi.width <= 0 || roi.height <= 0) {
        return input_image.clone();
    }
    cv::Mat cropped_ref = input_image(roi);
    return cropped_ref.clone();
}


// C++ function to rotate an image.
cv::Mat rotate_image(const cv::Mat& input_image, double angle) {
    cv::Point2f center(static_cast<float>(input_image.cols) / 2.0f, static_cast<float>(input_image.rows) / 2.0f);
    cv::Mat rot_mat = cv::getRotationMatrix2D(center, angle, 1.0);
    cv::Mat rotated_image;
    cv::warpAffine(input_image, rotated_image, rot_mat, input_image.size());
    return rotated_image;
}


// --- Python Wrappers ---

py::array_t<unsigned char> py_to_grayscale(py::array_t<unsigned char> input) {
    cv::Mat img = nparray_to_mat(input);
    cv::Mat result = to_grayscale(img);
    return mat_to_nparray(result);
}

py::array_t<unsigned char> py_apply_blur(py::array_t<unsigned char> input) {
    cv::Mat img = nparray_to_mat(input);
    cv::Mat result = apply_blur(img);
    return mat_to_nparray(result);
}

py::array_t<unsigned char> py_detect_edges(py::array_t<unsigned char> input) {
    cv::Mat img = nparray_to_mat(input);
    cv::Mat result = detect_edges(img);
    return mat_to_nparray(result);
}

py::array_t<unsigned char> py_sharpen_image(py::array_t<unsigned char> input) {
    cv::Mat img = nparray_to_mat(input);
    cv::Mat result = sharpen_image(img);
    return mat_to_nparray(result);
}

py::array_t<unsigned char> py_crop_image(py::array_t<unsigned char> input, int x, int y, int width, int height) {
    cv::Mat img = nparray_to_mat(input);
    cv::Mat result = crop_image(img, x, y, width, height);
    return mat_to_nparray(result);
}

py::array_t<unsigned char> py_rotate_image(py::array_t<unsigned char> input, double angle) {
    cv::Mat img = nparray_to_mat(input);
    cv::Mat result = rotate_image(img, angle);
    return mat_to_nparray(result);
}



PYBIND11_MODULE(visioncraft_cpp, m) {
    m.doc() = "High-performance image processing functions using C++ and OpenCV";

    m.def("to_grayscale", &py_to_grayscale, "Convert an image to grayscale");
    m.def("apply_blur", &py_apply_blur, "Apply Gaussian blur to an image");
    m.def("detect_edges", &py_detect_edges, "Detect edges using Canny algorithm");
    m.def("sharpen_image", &py_sharpen_image, "Sharpen an image");
    m.def("crop_image", &py_crop_image, "Crop an image to a given rectangle",
          py::arg("input"), py::arg("x"), py::arg("y"), py::arg("width"), py::arg("height"));
    m.def("rotate_image", &py_rotate_image, "Rotate an image by a given angle",
          py::arg("input"), py::arg("angle"));
}