#!/usr/bin/env python3
"""
claude-trimmer: Clean up trailing/leading spaces from Claude Code CLI terminal output.

Usage:
  claude-trimmer "your broken command here"   # Direct mode
  claude-trimmer                              # Interactive mode (paste, auto-submits, loops)
"""

import sys
import subprocess
import platform

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys


def clean_text(text: str) -> str:
    """Remove leading/trailing whitespace from each line and rejoin wrapped lines."""
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines]

    # Remove empty lines at start and end
    while cleaned_lines and cleaned_lines[0] == '':
        cleaned_lines.pop(0)
    while cleaned_lines and cleaned_lines[-1] == '':
        cleaned_lines.pop()

    if not cleaned_lines:
        return ''

    # Rejoin lines that were wrapped (continuation lines)
    result = []
    i = 0
    while i < len(cleaned_lines):
        current = cleaned_lines[i]

        # Keep joining next lines if they look like continuations
        while i + 1 < len(cleaned_lines):
            next_line = cleaned_lines[i + 1]

            # Empty line = paragraph break, stop joining
            if not next_line:
                break

            # Next line starts with special char = new item, stop joining
            if next_line and next_line[0] in '-*•>#0123456789':
                break

            # Next line starts with uppercase after period = new sentence, stop joining
            if current.endswith(('.', '!', '?', ':', '"', "'", ')')) and next_line and next_line[0].isupper():
                break

            # Next line is a closing delimiter = stop joining
            if next_line in ('EOF', ')', '}', ']', '```', "'''", '"""'):
                break

            # Current line ends with opening that expects content on same line
            if current.endswith(('(', '{', '[', '<<EOF', "<<'EOF'")):
                break

            # Looks like a continuation - join with space
            current = current + ' ' + next_line
            i += 1

        result.append(current)
        i += 1

    return '\n'.join(result)


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True on success."""
    try:
        if platform.system() == 'Darwin':
            subprocess.run(['pbcopy'], input=text.encode(), check=True)
            return True
        elif platform.system() == 'Linux':
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return False


def create_keybindings():
    """Create key bindings for the prompt."""
    bindings = KeyBindings()

    @bindings.add(Keys.ControlJ)  # Ctrl+J for newline
    def _(event):
        event.current_buffer.insert_text('\n')

    return bindings


def interactive_loop():
    """Run interactive loop - paste multiple times, Ctrl+C/Ctrl+D to exit."""
    print("=" * 50)
    print("claude-trimmer - Paste to trim, Ctrl+D to exit")
    print("Enter to submit, Ctrl+J for newline")
    print("=" * 50)

    session = PromptSession(
        multiline=False,
        key_bindings=create_keybindings(),
    )

    count = 0
    while True:
        try:
            count += 1
            text = session.prompt(f"\n[{count}] Paste: ")

            if not text.strip():
                print("(empty input, skipped)")
                count -= 1
                continue

            print("\n" + "-" * 30 + " OUTPUT " + "-" * 30)
            cleaned = clean_text(text)
            print(cleaned)

            if copy_to_clipboard(cleaned):
                print("-" * 68)
                print("[Copied to clipboard]")

        except (KeyboardInterrupt, EOFError):
            print("\n\nBye!")
            break


def main():
    if len(sys.argv) > 1:
        # Direct mode: argument provided
        text = ' '.join(sys.argv[1:])
        if not text.strip():
            print("No input provided.", file=sys.stderr)
            sys.exit(1)
        cleaned = clean_text(text)
        print(cleaned)
        if copy_to_clipboard(cleaned):
            print("\n[Copied to clipboard]", file=sys.stderr)
    else:
        # Interactive mode with loop
        interactive_loop()


if __name__ == '__main__':
    main()
