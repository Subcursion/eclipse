#include "os_util.h"
#include "io/file_util.h"

char* get_os_release() {
    return read_file("/etc/os-release");
}