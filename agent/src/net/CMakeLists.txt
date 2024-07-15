file(GLOB SRC_FILES 
    CONFIGURE_DEPENDS
    "*.c"
)

target_sources(eclipse PRIVATE ${SRC_FILES})