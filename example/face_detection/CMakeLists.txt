PROJECT(infer_demo C CXX)
CMAKE_MINIMUM_REQUIRED (VERSION 3.10)

option(FASTDEPLOY_INSTALL_DIR "Path of downloaded fastdeploy sdk.")
include(${FASTDEPLOY_INSTALL_DIR}/FastDeploy.cmake)
include_directories(${FASTDEPLOY_INCS})

add_executable(infer_scrfd ${PROJECT_SOURCE_DIR}/infer_scrfd.cc)
target_link_libraries(infer_scrfd ${FASTDEPLOY_LIBS})
