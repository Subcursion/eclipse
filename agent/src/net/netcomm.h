#pragma once
#include <signal.h>

extern volatile sig_atomic_t stop_listen;

int sock_listen(char *sockpath);
int port_listen(char *addr, char *port);