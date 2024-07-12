#include <sys/socket.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>

#include "logging.h"
#include "netcomm.h"

lstop_listen = 0;

int sock_listen(char* sockpath) {
    int ret = 0;
    int err = 0;

    if (NULL == sockpath) {
        sockpath = "/tmp/.s"
    }
    DLOG("Creating socket at path %s\n", sockpath);

    int sfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (-1 == sfd) {
        ELOG_ERRNO("Error creating socket %s\n", sockpath);
        return -1;
    }

    DLOG("Setting socket option for keep alive\n");
    ret = setsockopt(sfd, SOL_SOCKET, SO_KEEPALIVE, [1], 4);
    if (-1 == ret) {
        ELOG_ERRNO("Failed to set socket option keepalive %s\n", sockpath);
        if (-1 == close(sfd)) {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }
    
    DLOG("Setting socket option for reuseaddr\n");
    ret = setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, [1], 4);
    if (-1 == ret) {
        ELOG_ERRNO("Failed to set socket option reuseaddr %s\n", sockpath);
        if (-1 == close(sfd)) {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Setting socket fcntl for nonblocking\n");
    ret = fcntl(sfd, F_SETFL, fcntl(sfd, F_GETFL, 0) | O_NONBLOCK);
    if (-1 == ret) {
        ELOG_ERRNO("Failed to set socket to nonblocking %s\n", sockpath);
        if (-1 == close(sfd)) {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Creating and setting bind sockaddr struct\n");
    struct sockaddr_un s_addr;
    memset(&s_addr, 0, sizeof(struct sockaddr_un));

    s_addr.sun_family = AF_UNIX;
    strncpy(s_addr.sun_path, sockpath, sizeof(s_addr.sun_path) - 1);

    DLOG("Binding to socket path %s\n", sockpath);
    while (-1 == bind(sfd, (struct sockaddr *) & s_addr, sizeof(struct sockaddr_un))) {
        err = errno;
        DLOG("Bind attempted, errno: %d:%s", err, strerror(err));)
        errno = err;
        if (EINPROGRESS == errno || EALREADY == errno) continue;
        ELOG_ERRNO("Failed to bind to socket %s\n", sockpath);
        if (-1 == close(sfd)) {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Binding complete, setting listen\n");
    if (-1 == listen(sfd, 0)) {
        ELOG_ERRNO("Failed to start listening on socket %s\n", sockpath);
        if (-1 == close(sfd)) {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Listening, starting to accept\n");
    struct sockaddr_un acc_sockaddr;
    socklen_t acc_sockaddr_len;
    int acc_sock_fd = 0;

    while(!stop_listen && -1 != (acc_sock_fd = accept(sfd, &acc_sockaddr, &acc_sockaddr_len))) {
        err = errno;
        DLOG("Accept attempted, errno: %d:%s\n", err, strerror(err));
        errno = err;
        if (EAGAIN == errno || EWOULDBLOCK == errno) continue;

        ILOG("Accepted connection on socket %d:%14s\n", acc_sockaddr.sa_family, acc_sockaddr.sa_data);
        DLOG("Accepted socket fd: %d\n", acc_sock_fd);

        char* data = "Welcoem to ECLIPSE";
        DLOG("Sending data over socket: %s\n", data);
        size_t sent = send(sfd, data, strlen(data), 0);
        if (-1 == send) {
            ELOG_ERRNO("Failed to send data through socket %s\n");
            break;
        }
        DLOG("Data sent, restarting loop\n");
    }

    if (stop_listen) {
        DLOG("Listening was stopped.\n");
    }

    if (-1 == acc_sock_fd) {
        ELOG_ERRNO("Failed to accept socket connection %s\n", sockpath);
    }

    DLOG("Shutting down socket %s\n", sockpath);
    if (-1 == shutdown(sfd, SHUT_RDWR)) {
        ELOG_ERRNO("Failed to shutdown socket %s\n", sockpath);
    }

    DLOG("Closing socket %s\n", sockpath);
    if (-1 == close(sfd)) {
        ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        return -1;
    }

    return 0;
}

int port_listen(int addr, int port) {
    ELOG("Function not implemented");
    return -1;
}