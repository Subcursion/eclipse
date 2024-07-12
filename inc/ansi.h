#pragma once

#define ESCAPE "\e"
#define CSI ESCAPE "["

#define CSI_COLOR(n) CSI n "m"

#define COLOR_SEP ";"

#define RESET "0"
#define BOLD "1"
#define ITALIC "3"
#define UNDERLINE "4"

#define SET_STYLE(n) CSI_COLOR(n)

#define FG_BLACK "30"
#define FG_RED "31"
#define FG_GREEN "32"
#define FG_YELLOW "33"
#define FG_BLUE "34"
#define FG_MAGENTA "35"
#define FG_CYAN "36"
#define FG_WHITE "37"
#define BG_BLACK "40"
#define BG_RED "41"
#define BG_GREEN "42"
#define BG_YELLOW "43"
#define BG_BLUE "44"
#define BG_MAGENTA "45"
#define BG_CYAN "46"
#define BG_WHITE "47"
#define FG_BRIGHT_BLACK "90"
#define FG_BRIGHT_RED "91"
#define FG_BRIGHT_GREEN "92"
#define FG_BRIGHT_YELLOW "93"
#define FG_BRIGHT_BLUE "94"
#define FG_BRIGHT_MAGENTA "95"
#define FG_BRIGHT_CYAN "96"
#define FG_BRIGHT_WHITE "97"
#define BG_BRIGHT_BLACK "100"
#define BG_BRIGHT_RED "101"
#define BG_BRIGHT_GREEN "102"
#define BG_BRIGHT_YELLOW "103"
#define BG_BRIGHT_BLUE "104"
#define BG_BRIGHT_MAGENTA "105"
#define BG_BRIGHT_CYAN "106"
#define BG_BRIGHT_WHITE "107"

#define RESET_COLOR CSI_COLOR(RESET COLOR_SEP RESET)
#define SET_COLOR_4BIT(fg, bg) CSI_COLOR(fg COLOR_SEP bg)

#define BIT_8 "5"
#define BIT_24 "2"
#define FG_8BIT "38"
#define BG_8BIT "48"

#define SET_FG_8BIT(n) CSI_COLOR(FG_8BIT COLOR_SEP BIT_8 COLOR_SEP n)
#define SET_BG_8BIT(n) CSI_COLOR(BG_8BIT COLOR_SEP BIT_8 COLOR_SEP n)

#define SET_FG_COLOR(r, g, b) CSI_COLOR(FG_8BIT COLOR_SEP BIT_24 COLOR_SEP r COLOR_SEP g COLOR_SEP b)
#define SET_BG_COLOR(r, g, b) CSI_COLOR(BG_8BIT COLOR_SEP BIT_24 COLOR_SEP r COLOR_SEP g COLOR_SEP b)
