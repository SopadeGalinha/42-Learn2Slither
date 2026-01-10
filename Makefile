.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: all lib install clean fclean re test info help

# Default target
all: lib install

# Build C library
lib:
	@cd c_src && $(MAKE) all

# Install Python package (creates 'snake' command)
install: lib
	@echo "Installing Python package..."
	@pip install -e . -q
	@echo "✓ 'snake' command installed"

# Uninstall Python package
uninstall:
	@echo "Uninstalling Python package..."
	@pip uninstall -y learn2slither 2>/dev/null || true
	@rm -rf *.egg-info
	@echo "✓ Python package uninstalled"

# Run C tests
test:
	@cd c_src && $(MAKE) test

# Run Python tests
pytest:
	@python -m pytest tests/ -v

# Clean build artifacts
clean:
	@cd c_src && $(MAKE) clean
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Full clean (remove library + uninstall)
fclean: uninstall
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
	@echo "make              - Build C library + install Python package"
	@echo "make lib          - Build C library only"
	@echo "make install      - Install Python package (creates 'snake' command)"
	@echo "make uninstall    - Uninstall Python package"
	@echo "make test         - Run C tests"
	@echo "make pytest       - Run Python tests"
	@echo "make clean        - Remove build objects + __pycache__"
	@echo "make fclean       - Remove all artifacts + uninstall package"
	@echo "make re           - Full rebuild (fclean + all)"
	@echo "make info         - Show build configuration"
	@echo "make help         - Show this help"
	@echo ""
	@echo "After 'make', you can run:"
	@echo "  snake -visual on -sessions 10"
	@echo "  snake -load models/qtable-10000.json -visual on -dontlearn"
