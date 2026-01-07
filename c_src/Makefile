.SILENT:
MAKEFLAGS += --no-print-directory

CC := cc
CFLAGS := -Wall -Wextra -Werror

C_SRC_DIR := board
BUILD_DIR := ../build
LIBDIR := ../lib

NAME := $(LIBDIR)/libboard.so

SOURCES := $(C_SRC_DIR)/board.c \
		   $(C_SRC_DIR)/board_apples.c \
		   $(C_SRC_DIR)/board_move.c \
		   $(C_SRC_DIR)/board_query.c \
		   $(C_SRC_DIR)/board_state.c \
		   $(C_SRC_DIR)/board_helpers.c \
		   $(C_SRC_DIR)/board_setup.c \
		   $(C_SRC_DIR)/rewards.c

OBJECTS := $(BUILD_DIR)/board.o \
		   $(BUILD_DIR)/board_apples.o \
		   $(BUILD_DIR)/board_move.o \
		   $(BUILD_DIR)/board_query.o \
		   $(BUILD_DIR)/board_state.o \
		   $(BUILD_DIR)/board_helpers.o \
		   $(BUILD_DIR)/board_setup.o \
		   $(BUILD_DIR)/rewards.o

.PHONY: all clean fclean re info test

all: $(NAME)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(LIBDIR):
	mkdir -p $(LIBDIR)

$(BUILD_DIR)/board.o: $(C_SRC_DIR)/board.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_apples.o: $(C_SRC_DIR)/board_apples.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_move.o: $(C_SRC_DIR)/board_move.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_query.o: $(C_SRC_DIR)/board_query.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_state.o: $(C_SRC_DIR)/board_state.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_helpers.o: $(C_SRC_DIR)/board_helpers.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_setup.o: $(C_SRC_DIR)/board_setup.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/rewards.o: $(C_SRC_DIR)/rewards.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(NAME): $(OBJECTS) | $(LIBDIR)
	$(CC) $(CFLAGS) -shared $^ -o $@

test:
	@cd tests && $(MAKE) test

clean:
	rm -f $(OBJECTS)

fclean: clean
	rm -rf $(BUILD_DIR) $(LIBDIR)

re: fclean all

info:
	@echo "CC: $(CC)"
	@echo "CFLAGS: $(CFLAGS)"
	@echo "NAME: $(NAME)"
