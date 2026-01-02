#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip to ensure we can handle modern binary wheels
pip install --upgrade pip setuptools wheel

# Install dependencies
# --prefer-binary: forces pip to use a pre-compiled wheel even if it's slightly older, 
# preventing the "Rust compilation" error.
pip install -r requirements.txt --prefer-binary
