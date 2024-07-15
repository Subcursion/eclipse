#pragma once

#include <stdio.h>
#include <errno.h>
#include <string.h>

#include "ansi.h"

#define DEBUG_SYMBOL SET_FG_8BIT("33") "^" RESET_COLOR
#define SUCCESS_SYMBOL SET_FG_8BIT("46") "+" RESET_COLOR
#define INFO_SYMBOL SET_FG_8BIT("246") "*" RESET_COLOR
#define WARNING_SYMBOL SET_FG_8BIT("208") "!" RESET_COLOR
#define ERROR_SYMBOL SET_STYLE(BOLD) SET_FG_8BIT("196") "-" RESET_COLOR
#define LOG_FORMAT "[%s]" SET_FG_8BIT("244") " %s:%d|%s: " RESET_COLOR

#ifdef DEBUG
#define DLOG(format, ...) fprintf(stdout, LOG_FORMAT format, DEBUG_SYMBOL, __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
#define DLOG(format, ...)
#endif

#ifdef DEBUG
#define SLOG(format, ...) fprintf(stdout, LOG_FORMAT format, SUCCESS_SYMBOL, __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
#define SLOG(format, ...)
#endif

#ifdef DEBUG
#define ILOG(format, ...) fprintf(stdout, LOG_FORMAT format, INFO_SYMBOL, __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
#define ILOG(format, ...)
#endif

#ifdef DEBUG
#define WLOG(format, ...) fprintf(stderr, LOG_FORMAT format, WARNING_SYMBOL, __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
#define WLOG(format, ...)
#endif

#ifdef DEBUG
#define ELOG(format, ...) fprintf(stderr, LOG_FORMAT format, ERROR_SYMBOL, __FILE__, __LINE__, __func__, ##__VA_ARGS__)
#else
#define ELOG(format, ...)
#endif

#ifdef DEBUG
#define ELOG_ERRNO(format, ...) fprintf(stderr, LOG_FORMAT format "%s/%d:%s\n", ERROR_SYMBOL, __FILE__, __LINE__, __func__, ##__VA_ARGS__, strerrorname_np(errno), errno, strerror(errno))
#else
#define ELOG_ERRNO(format, ...)
#endif