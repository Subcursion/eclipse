
file(GLOB SRC_FILES 
    CONFIGURE_DEPENDS
    "*.c"
)

target_include_directories(eclipse PRIVATE ./)
target_sources(eclipse PRIVATE ${SRC_FILES})

add_subdirectory(io)
add_subdirectory(net)