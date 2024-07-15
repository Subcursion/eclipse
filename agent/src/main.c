#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>

#include "ansi.h"
#include "logging.h"
#include "os_util.h"
#include "net/netcomm.h"
#include "sig_util.h"

int main(int argc, char *argv[])
{
    ILOG("Welcome to Eclipse - The Shadow in the System\n");

    DLOG("Setting up SIGINT catching\n");

    struct sigaction action;
    memset(&action, 0, sizeof(action));
    action.sa_handler = sigaction_func;
    if (-1 == sigaction(SIGINT, &action, NULL))
    {
        ELOG_ERRNO("Failed to set sigaction\n");
        return -1;
    }

    ILOG("Getting os release information\n");

    char *os_release = get_os_release();
    if (NULL == os_release)
    {
        ELOG("Failed to get os release information\n");
        return -1;
    }
    SLOG("OS Release: %s\n", os_release);

    DLOG("Freeing os release memory\n");
    free(os_release);

    ILOG("Starting up port server\n");

    int ret = port_listen(NULL, "2222");
    if (-1 == ret)
    {
        ELOG("Port listening failed.\n");
        return -1;
    }

    ILOG("Exiting\n");

    return 0;
}