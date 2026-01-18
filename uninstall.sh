#!/bin/bash
set -e

echo "Uninstalling claude-trimmer..."

pip3 uninstall -y claude-trimmer

echo ""
echo "Done! Note: PATH entry in your shell config was left intact."
echo "You can remove the '# Added by claude-trimmer installer' lines manually if desired."
