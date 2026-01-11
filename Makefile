.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: all lib clean fclean re test info help

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
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Full clean
fclean:
	@cd c_src && $(MAKE) fclean
	@rm -rf *.egg-info
	@rm -rf .pytest_cache
	@echo "✓ Full clean complete"

# Full rebuild
re: fclean all

# Show build info
info:
	@cd c_src && $(MAKE) info
	@echo ""
	@echo "Python Package:"
	@which snake 2>/dev/null && echo "  snake command: $$(which snake)" || echo "  snake command: not installed (run 'make install')"

# Help
help:
	@echo "Learn2Slither - Build Commands"
	@echo "================================"
	@echo "make              - Run default target (all)"
	@echo "make lib          - Build C library"
	@echo "make test         - Run C tests"
	@echo "make clean        - Remove build objects + __pycache__"
	@echo "make fclean       - Remove all artifacts"
	@echo "make re           - Full rebuild (fclean + all)"
	@echo "make info         - Show build configuration"
	@echo "make help         - Show this help"
	@echo ""
