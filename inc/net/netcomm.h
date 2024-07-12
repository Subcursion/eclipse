#pragma once
#include <signal.h>

volatile sig_atomic_t stop_listen;

int sock_listen(char* sockpath);
int port_listen(int addr, int port);