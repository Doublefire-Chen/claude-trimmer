#!/bin/bash
set -e

echo "Installing claude-trimmer..."

# Detect OS
OS="$(uname -s)"
echo "Detected OS: $OS"

# Install the package with --user flag
pip3 install --user . --no-warn-script-location

# Get the scripts directory based on OS
case "$OS" in
    Linux*)
        SCRIPTS_DIR="$HOME/.local/bin"
        ;;
    Darwin*)
        # macOS - get actual path from Python
        SCRIPTS_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_path('scripts', 'posix_user'))")
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # Windows Git Bash / MSYS
        SCRIPTS_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))")
        ;;
    *)
        echo "Unknown OS: $OS"
        SCRIPTS_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_path('scripts'))")
        ;;
esac

echo "Scripts installed to: $SCRIPTS_DIR"

# Verify the script exists
if [ ! -f "$SCRIPTS_DIR/claude-trimmer" ]; then
    echo "Warning: claude-trimmer not found at expected location"
    echo "You may need to add the Python scripts directory to your PATH manually"
    exit 1
fi

# Check if already in PATH
if [[ ":$PATH:" == *":$SCRIPTS_DIR:"* ]]; then
    echo "Directory already in PATH. You're all set!"
else
    # Detect shell config file
    case "$OS" in
        Darwin*)
            # macOS defaults to zsh since Catalina
            if [ -f "$HOME/.zshrc" ]; then
                SHELL_RC="$HOME/.zshrc"
            elif [ -f "$HOME/.bash_profile" ]; then
                SHELL_RC="$HOME/.bash_profile"
            else
                SHELL_RC="$HOME/.zshrc"
            fi
            ;;
        Linux*)
            if [ -f "$HOME/.bashrc" ]; then
                SHELL_RC="$HOME/.bashrc"
            elif [ -f "$HOME/.zshrc" ]; then
                SHELL_RC="$HOME/.zshrc"
            else
                SHELL_RC="$HOME/.profile"
            fi
            ;;
        *)
            SHELL_RC="$HOME/.profile"
            ;;
    esac

    # Check if already added to shell config
    if grep -q "$SCRIPTS_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "PATH already configured in $SHELL_RC"
    else
        echo "" >> "$SHELL_RC"
        echo "# Added by claude-trimmer installer" >> "$SHELL_RC"
        echo "export PATH=\"$SCRIPTS_DIR:\$PATH\"" >> "$SHELL_RC"
        echo "Added PATH to $SHELL_RC"
    fi

    echo ""
    echo "Run this to use immediately (or restart your terminal):"
    echo "  source $SHELL_RC"
fi

echo ""
echo "Done! Use: claude-trimmer \"your text\""
