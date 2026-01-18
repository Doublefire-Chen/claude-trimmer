from setuptools import setup, find_packages

setup(
    name="claude-trimmer",
    version="0.1.0",
    description="Clean up trailing/leading spaces from Claude Code CLI terminal output",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AkaCyberRat/claude-trimmer",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "prompt_toolkit>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "claude-trimmer=claude_trimmer.cli:main",
        ],
    },
    license="AGPL-3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
