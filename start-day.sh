#!/bin/bash
# -----------------------------
# Run main.py from its directory
# -----------------------------

# Automatically detect where this shell script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"          # Folder where main.py lives
SCRIPT_NAME="main.py"              # Name of your Python script
VENV_PATH=".venv/Scripts/activate" # Path to virtual environment

# Change to the project directory
cd "$PROJECT_DIR" || {
    echo "❌ Failed to change directory to $PROJECT_DIR"
    exit 1
}

# Activate virtual environment
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
else
    echo "⚠️ Virtual environment not found at $VENV_PATH"
fi

# Run Python script
python "$SCRIPT_NAME"

# Deactivate virtual environment
deactivate 2>/dev/null || true
