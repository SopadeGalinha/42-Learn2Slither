.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: all lib clean fclean re test valgrind info help

# Default target
all: lib

# Build C library
lib:
	@cd c_src && $(MAKE) all

# Run C tests
test:
	@cd c_src && $(MAKE) test

# Clean build artifacts
clean:
	@cd c_src && $(MAKE) clean

# Full clean (remove library)
fclean:
	@cd c_src && $(MAKE) fclean

# Full rebuild
re:
	@cd c_src && $(MAKE) re

# Show build info
info:
	@cd c_src && $(MAKE) info

# Help
help:
	@echo "Learn2Slither - Build Commands"
	@echo "================================"
	@echo "make lib          - Build C library (default)"
	@echo "make test         - Run C tests"
	@echo "make valgrind     - Run C tests with memory leak detection"
	@echo "make clean        - Remove build objects"
	@echo "make fclean       - Remove all build artifacts + library"
	@echo "make re           - Full rebuild (fclean + all)"
	@echo "make info         - Show build configuration"
	@echo "make help         - Show this help"
	@echo ""
	@echo "Python (requires PYTHONPATH setup):"
	@echo "  python3 tests/test.py           - Run Python tests"
	@echo "  python3 scripts/train.py --help - Show training options"
