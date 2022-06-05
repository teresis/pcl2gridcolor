cmake_minimum_required(VERSION 2.8)
project(pcl2grid)

find_package(OpenCV 3.0 QUIET)
include_directories(${OpenCV_INCLUDE_DIR})


# Build examples


add_executable(pcl2grid
src/test.cpp)
target_link_libraries(pcl2grid ${OpenCV_LIBRARIES})


