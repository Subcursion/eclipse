cmake_minimum_required(VERSION 3.10)

project(eclipse
    VERSION 0.1
    LANGUAGES C
)

add_executable(eclipse)

set_target_properties( eclipse
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    # allows -DCMAKE_BUILD_TYPE=Debug to be specified to make a debug build in another folder
    RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}/bin/debug"
)

target_compile_options(eclipse PRIVATE -Wall)
target_compile_options(eclipse PRIVATE -Werror)

# for -DCMAKE_BUILD_TYPE=Debug to get defined in the preprocessor
target_compile_definitions(eclipse PRIVATE
    $<$<CONFIG:Debug>:DEBUG=1>
    _GNU_SOURCE
)

add_subdirectory(src)
