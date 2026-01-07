.SILENT:
MAKEFLAGS += --no-print-directory

CC := cc
CFLAGS := -Wall -Wextra -Werror

TESTS_DIR := .
BOARD_DIR := ../board
BUILD_DIR := ../../build

# Core board files needed for tests
BOARD_SOURCES := $(BOARD_DIR)/board.c \
                 $(BOARD_DIR)/board_apples.c \
                 $(BOARD_DIR)/board_move.c \
                 $(BOARD_DIR)/board_query.c \
                 $(BOARD_DIR)/board_state.c \
                 $(BOARD_DIR)/board_helpers.c \
                 $(BOARD_DIR)/board_setup.c \
                 $(BOARD_DIR)/rewards.c

# Test files
TEST_SOURCES := $(TESTS_DIR)/test_board_creation.c \
                $(TESTS_DIR)/test_board_edge_cases.c \
                $(TESTS_DIR)/test_board_validation.c \
                $(TESTS_DIR)/test_board_memory.c \
                $(TESTS_DIR)/test_runner.c \
                $(TESTS_DIR)/test_helpers.c

TEST_OBJECTS := $(BUILD_DIR)/test_board_creation.o \
                $(BUILD_DIR)/test_board_edge_cases.o \
                $(BUILD_DIR)/test_board_validation.o \
                $(BUILD_DIR)/test_board_memory.o \
                $(BUILD_DIR)/test_runner.o \
                $(BUILD_DIR)/test_helpers.o

BOARD_OBJECTS := $(BUILD_DIR)/board.o \
                 $(BUILD_DIR)/board_apples.o \
                 $(BUILD_DIR)/board_move.o \
                 $(BUILD_DIR)/board_query.o \
                 $(BUILD_DIR)/board_state.o \
                 $(BUILD_DIR)/board_helpers.o \
                 $(BUILD_DIR)/board_setup.o \
                 $(BUILD_DIR)/rewards.o

TEST_EXEC := $(BUILD_DIR)/test_suite

.PHONY: all test clean fclean valgrind

all: test

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/test_board_creation.o: $(TESTS_DIR)/test_board_creation.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_board_edge_cases.o: $(TESTS_DIR)/test_board_edge_cases.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_board_validation.o: $(TESTS_DIR)/test_board_validation.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_board_memory.o: $(TESTS_DIR)/test_board_memory.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_runner.o: $(TESTS_DIR)/test_runner.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_helpers.o: $(TESTS_DIR)/test_helpers.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/board.o: $(BOARD_DIR)/board.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_apples.o: $(BOARD_DIR)/board_apples.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_move.o: $(BOARD_DIR)/board_move.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_query.o: $(BOARD_DIR)/board_query.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_state.o: $(BOARD_DIR)/board_state.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_helpers.o: $(BOARD_DIR)/board_helpers.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/board_setup.o: $(BOARD_DIR)/board_setup.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/rewards.o: $(BOARD_DIR)/rewards.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(TEST_EXEC): $(BOARD_OBJECTS) $(TEST_OBJECTS)
	$(CC) $(CFLAGS) $^ -o $@

test: $(TEST_EXEC)
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./$(TEST_EXEC)

clean:
	rm -f $(TEST_OBJECTS) $(BOARD_OBJECTS)

fclean: clean
	rm -f $(TEST_EXEC)
