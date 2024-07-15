
#include <signal.h>

#include "net/netcomm.h"

void sigaction_func(int signal) {
    // disable sockets listening
    stop_listen = 1;
}