SRC_DIR := src
INC_DIR := inc
OBJ_DIR := obj
BIN_DIR := bin

BINARY := $(BIN_DIR)/eclipse
SRC := $(wildcard $(SRC_DIR)/*.c)
OBJ := $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)


CPPFLAGS := -I$(INC_DIR) -MMD -MP
CLFAGS := -Wall
LDFLAGS :=  # like -Llib
LDLIBS :=  # like -lm
DFLAGS := -DDEBUG -g

.PHONY: all clean

all: $(BINARY)


$(BINARY): $(OBJ) | $(BIN_DIR)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BIN_DIR) $(OBJ_DIR):
	mkdir -p $@

clean:
	@$(RM) -rv $(BIN_DIR) $(OBJ_DIR)