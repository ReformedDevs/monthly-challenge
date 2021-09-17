#!/usr/bin/env bash
set -euo pipefail

poetry shell && python3 verifier.py --server https://mineswepttd.0x44.pw --dump '123.45 F
1
Lose!
1 1 1
hardly-hopelessly-fancy-rhino
01'
