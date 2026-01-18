# claude-trimmer

Clean up trailing/leading spaces from Claude Code CLI terminal output.

When copying text from Claude Code terminal, extra spaces are often added to each line and lines may be broken mid-sentence. This tool strips spaces and rejoins wrapped lines.

## Features

- Strips leading/trailing whitespace from each line
- Rejoins lines that were wrapped due to terminal width
- Interactive loop mode (paste multiple times without restarting)
- Auto-copies cleaned text to clipboard (macOS/Linux)
- Uses `prompt_toolkit` for proper paste detection

## Installation

```bash
git clone https://github.com/Doublefire-Chen/claude-trimmer
cd claude-trimmer
./install.sh
```

## Usage

### Direct Mode
```bash
claude-trimmer "your broken command here"
```

### Interactive Mode
```bash
claude-trimmer
```

- **Paste** your text
- **Enter** to submit
- **Ctrl+J** to insert a newline manually
- **Ctrl+C** or **Ctrl+D** to exit

### Example

Input (with trailing spaces and broken lines):
```
git commit -m "$(cat <<'EOF'
  Refactor SyncScheduler to use job processor
  for scheduled syncs
  EOF
  )"
```

Output (cleaned and rejoined):
```
git commit -m "$(cat <<'EOF'
Refactor SyncScheduler to use job processor for scheduled syncs
EOF
)"
```

The cleaned text is automatically copied to your clipboard.

### Uninstall

```bash
./uninstall.sh
```

## Why?

This is a known issue with Claude Code CLI:
- [#4686](https://github.com/anthropics/claude-code/issues/4686)
- [#15199](https://github.com/anthropics/claude-code/issues/15199)

Until Anthropic fixes it, this tool provides a quick workaround.

## License

AGPL-3.0
