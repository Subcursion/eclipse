#include <sys/socket.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/un.h>
#include <netdb.h>
#include <arpa/inet.h>

#include "logging.h"
#include "netcomm.h"

volatile sig_atomic_t stop_listen = 0;

int sock_listen(char *sockpath)
{
    int ret = 0;
    int err = 0;

    if (NULL == sockpath)
    {
        sockpath = "/tmp/.s";
    }
    DLOG("Creating socket at path %s\n", sockpath);

    int sfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (-1 == sfd)
    {
        ELOG_ERRNO("Error creating socket %s\n", sockpath);
        return -1;
    }

    DLOG("Setting socket option for keep alive\n");
    int sock_opt_value = 1;
    ret = setsockopt(sfd, SOL_SOCKET, SO_KEEPALIVE, &sock_opt_value, sizeof(sock_opt_value));
    if (-1 == ret)
    {
        ELOG_ERRNO("Failed to set socket option keepalive %s\n", sockpath);
        if (-1 == close(sfd))
        {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Setting socket option for reuseaddr\n");
    ret = setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &sock_opt_value, sizeof(sock_opt_value));
    if (-1 == ret)
    {
        ELOG_ERRNO("Failed to set socket option reuseaddr %s\n", sockpath);
        if (-1 == close(sfd))
        {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Setting socket fcntl for nonblocking\n");
    ret = fcntl(sfd, F_SETFL, fcntl(sfd, F_GETFL, 0) | O_NONBLOCK);
    if (-1 == ret)
    {
        ELOG_ERRNO("Failed to set socket to nonblocking %s\n", sockpath);
        if (-1 == close(sfd))
        {
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
    while (-1 == bind(sfd, (struct sockaddr *)&s_addr, sizeof(s_addr)))
    {
        err = errno;
        DLOG("Bind attempted, errno: %d:%s\n", err, strerror(err));
        errno = err;
        if (EINPROGRESS == errno || EALREADY == errno)
            continue;
        ELOG_ERRNO("Failed to bind to socket %s\n", sockpath);
        if (-1 == close(sfd))
        {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Binding complete, setting listen\n");
    if (-1 == listen(sfd, 10))
    {
        ELOG_ERRNO("Failed to start listening on socket %s\n", sockpath);
        if (-1 == close(sfd))
        {
            ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        }
        return -1;
    }

    DLOG("Listening, starting to accept\n");
    struct sockaddr_un acc_sockaddr;
    socklen_t acc_sockaddr_len = sizeof(acc_sockaddr);
    int acc_sock_fd = 0;

    while (!stop_listen)
    {
        errno = 0;
        acc_sock_fd = accept(sfd, (struct sockaddr *)&acc_sockaddr, &acc_sockaddr_len);
        if (EAGAIN == errno || EWOULDBLOCK == errno)
            continue;
        if (-1 == acc_sock_fd)
            break;

        ILOG("Accepted connection on socket %d:%108s\n", acc_sockaddr.sun_family, acc_sockaddr.sun_path);
        DLOG("Accepted socket fd: %d\n", acc_sock_fd);

        char *data = "Welcome to ECLIPSE\n";
        DLOG("Sending data over socket: %s", data);
        size_t sent = send(acc_sock_fd, data, strlen(data), 0);
        if (-1 == sent)
        {
            ELOG_ERRNO("Failed to send data through socket %s\n", sockpath);
            break;
        }
        DLOG("Data sent, closing accepted socket %d\n", acc_sock_fd);
        if (-1 == close(acc_sock_fd))
        {
            ELOG("Failed to close accepted socket %d\n", acc_sock_fd);
        }
    }

    if (stop_listen)
    {
        DLOG("Listening was stopped.\n");
    }

    if (!stop_listen && -1 == acc_sock_fd)
    {
        ELOG_ERRNO("Failed to accept socket connection %s\n", sockpath);
    }

    DLOG("Shutting down socket %s\n", sockpath);
    if (-1 == shutdown(sfd, SHUT_RDWR))
    {
        ELOG_ERRNO("Failed to shutdown socket %s\n", sockpath);
    }

    DLOG("Closing socket %s\n", sockpath);
    if (-1 == close(sfd))
    {
        ELOG_ERRNO("Failed to close socket %s\n", sockpath);
        return -1;
    }

    DLOG("Removing socket %s\n", sockpath);
    if (-1 == unlink(sockpath))
    {
        ELOG_ERRNO("Failed to remove socket %s, manually cleaning may be required.\n", sockpath);
        return -1;
    }

    return 0;
}

int port_listen(char *addr, char *port)
{
    int ret = 0;
    int err = 0;
    int sfd;

    struct sockaddr_in sockname;
    socklen_t socklen = sizeof(sockname);
    struct addrinfo hints;
    struct addrinfo *result, *rp;

    if (NULL == port)
    {
        ELOG("Port cannot be NULL\n");
        return -1;
    }

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE | AI_NUMERICSERV; // any interface + only port strings, no names
    hints.ai_protocol = 0;                        // any proto
    hints.ai_canonname = NULL;
    hints.ai_addr = NULL;
    hints.ai_next = NULL;

    ret = getaddrinfo(addr, port, &hints, &result);
    if (0 != ret)
    {
        ELOG("Failed to get address information: %d:%s\n", ret, gai_strerror(ret));
        return -1;
    }

    for (rp = result; rp != NULL; rp = rp->ai_next)
    {
        DLOG("Attempting socket creation with params %d:%d%d\n", rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        sfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (-1 == sfd)
        {
            DLOG("Socket creation failed, trying next\n");
            continue;
        }

        DLOG("Setting socket option for keep alive\n");
        int sock_opt_value = 1;
        ret = setsockopt(sfd, SOL_SOCKET, SO_KEEPALIVE, &sock_opt_value, sizeof(sock_opt_value));
        if (-1 == ret)
        {
            ELOG_ERRNO("Failed to set socket option keepalive %d\n", sfd);
            if (-1 == close(sfd))
            {
                ELOG_ERRNO("Failed to close socket %d\n", sfd);
            }
            continue;
        }

        DLOG("Setting socket option for reuseaddr\n");
        ret = setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &sock_opt_value, sizeof(sock_opt_value));
        if (-1 == ret)
        {
            ELOG_ERRNO("Failed to set socket option reuseaddr %d\n", sfd);
            if (-1 == close(sfd))
            {
                ELOG_ERRNO("Failed to close socket %d\n", sfd);
            }
            continue;
        }

        DLOG("Setting socket fcntl for nonblocking\n");
        ret = fcntl(sfd, F_SETFL, fcntl(sfd, F_GETFL, 0) | O_NONBLOCK);
        if (-1 == ret)
        {
            ELOG_ERRNO("Failed to set socket to nonblocking %d\n", sfd);
            if (-1 == close(sfd))
            {
                ELOG_ERRNO("Failed to close socket %d\n", sfd);
            }
            continue;
        }

        DLOG("Binding to socket %d\n", sfd);
        while (-1 == (ret = bind(sfd, rp->ai_addr, rp->ai_addrlen)))
        {
            err = errno;
            DLOG("Bind attempted, errno: %d:%s\n", err, strerror(err));
            errno = err;
            if (EINPROGRESS == errno || EALREADY == errno)
                continue;
            ELOG_ERRNO("Failed to bind to socket %d\n", sfd);
            break;
        }

        if (-1 != ret)
        { // success bind
            break;
        }

        ret = close(sfd);
        if (-1 == ret)
        {
            ELOG_ERRNO("Failed to close socket %d\n", sfd);
        }
    }

    freeaddrinfo(result);

    if (NULL == rp)
    {
        ELOG("Failed to bind to any addresses\n");
        return -1;
    }

    DLOG("Binding complete, setting listen\n");
    if (-1 == listen(sfd, 10))
    {
        ELOG_ERRNO("Failed to start listening on socket %d\n", sfd);
        if (-1 == close(sfd))
        {
            ELOG_ERRNO("Failed to close socket %d\n", sfd);
        }
        return -1;
    }

    if (-1 == getsockname(sfd, &sockname, &socklen))
    {
        ELOG_ERRNO("Failed to get socket address\n");
        if (-1 == close(sfd))
        {
            ELOG_ERRNO("Failed to close socket %d\n", sfd);
        }
        return -1;
    }

    ILOG("Listening on %s:%d\n", inet_ntoa(sockname.sin_addr), ntohs(sockname.sin_port));

    struct sockaddr_in acc_sockaddr;
    socklen_t acc_sockaddr_len = sizeof(acc_sockaddr);
    int acc_sock_fd = 0;

    while (!stop_listen)
    {
        errno = 0;
        acc_sock_fd = accept(sfd, (struct sockaddr *)&acc_sockaddr, &acc_sockaddr_len);
        if (EAGAIN == errno || EWOULDBLOCK == errno)
            continue;
        if (-1 == acc_sock_fd)
            break;

        ILOG("Accepted connection at %s:%d\n", inet_ntoa(acc_sockaddr.sin_addr), acc_sockaddr.sin_port);
        DLOG("Accepted socket fd: %d\n", acc_sock_fd);

        char *data = "Welcome to ECLIPSE\n";
        DLOG("Sending data over socket: %s", data);
        size_t sent = send(acc_sock_fd, data, strlen(data), 0);
        if (-1 == sent)
        {
            ELOG_ERRNO("Failed to send data\n");
            break;
        }
        DLOG("Data sent, closing accepted socket\n");
        if (-1 == close(acc_sock_fd))
        {
            ELOG("Failed to close accepted socket\n");
        }
    }

    if (stop_listen)
    {
        DLOG("Listening was stopped.\n");
    }

    if (!stop_listen && -1 == acc_sock_fd)
    {
        ELOG_ERRNO("Failed to accept connection\n");
    }

    DLOG("Shutting down socket\n");
    if (-1 == shutdown(sfd, SHUT_RDWR))
    {
        ELOG_ERRNO("Failed to shutdown socket\n");
    }

    DLOG("Closing socket\n");
    if (-1 == close(sfd))
    {
        ELOG_ERRNO("Failed to close socket\n");
        return -1;
    }

    return 0;
}