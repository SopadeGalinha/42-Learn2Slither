CC := gcc
CFLAGS := -Wall -Wextra -Werror -g -fPIC -std=c99
LDFLAGS := -shared

# Directories
C_SRC_DIR := c_src/board
BUILD_DIR := build
LIBDIR := lib

# Sources
C_SOURCES := $(C_SRC_DIR)/board.c
TEST_SOURCES := $(C_SRC_DIR)/test_board.c
OBJECTS := $(BUILD_DIR)/board.o

# Targets
SHARED_LIB := $(LIBDIR)/libboard.so
TEST_EXEC := $(BUILD_DIR)/test_board

.PHONY: all clean test lib dirs help format lint

# ==================== DEFAULT TARGET ====================

all: lib test
	@echo "✓ Build complete"

help:
	@echo "Available targets:"
	@echo "  make lib        - Build C library"
	@echo "  make test       - Run C tests"
	@echo "  make format     - Format code (C and Python)"
	@echo "  make lint       - Check code style"
	@echo "  make clean      - Remove build artifacts"

# ==================== BUILD TARGETS ====================

lib: dirs $(SHARED_LIB)

test: lib $(TEST_EXEC)
	@echo "Running tests..."
	@$(TEST_EXEC)

dirs:
	@mkdir -p $(BUILD_DIR) $(LIBDIR)

$(BUILD_DIR)/board.o: $(C_SOURCES) | dirs
	$(CC) $(CFLAGS) -c $< -o $@

$(SHARED_LIB): $(OBJECTS) | dirs
	$(CC) $(CFLAGS) $(LDFLAGS) $^ -o $@
	@echo "✓ Shared library built: $@"

$(TEST_EXEC): $(OBJECTS) $(TEST_SOURCES) | dirs
	$(CC) $(CFLAGS) $^ -o $@
	@echo "✓ Test executable built: $@"

# ==================== CODE QUALITY ====================

format:
	@echo "Formatting C code..."
	@clang-format -i $(C_SOURCES) $(TEST_SOURCES)
	@echo "Formatting Python code..."
	@find . -name "*.py" -type f ! -path "./venv/*" ! -path "./build/*" -exec python3 -m black {} \;
	@echo "✓ Code formatted"

lint:
	@echo "Checking code style..."
	@find . -name "*.py" -type f ! -path "./venv/*" ! -path "./build/*" -exec python3 -m flake8 {} \;
	@echo "✓ Style check complete"

# ==================== CLEANUP ====================

clean:
	@rm -rf $(BUILD_DIR) $(LIBDIR)
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned build artifacts"

# ==================== INFO ====================

info:
	@echo "CC: $(CC)"
	@echo "CFLAGS: $(CFLAGS)"
	@echo "Sources: $(C_SOURCES)"
	@echo "Shared Lib: $(SHARED_LIB)"
	@echo "Test Exec: $(TEST_EXEC)"
