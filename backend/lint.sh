# Check if "python3" command is available
if command -v python3 &>/dev/null; then
    # Run with Python 3
    python3 -m ruff check .
else
    # Run with Python 2 (assuming it's available)
    python -m ruff check .
fi
