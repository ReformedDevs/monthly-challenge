#!/usr/bin/env bash
set -euo pipefail

poetry shell && python3 updater.py --server https://mineswepttd.0x44.pw \
                                  --author "test-man" \
                                  --run "1" \
                                  --configmap_path 'testcm.yaml' \
                                  --dump '123.45 F
1
Win!
1 1 1
hardly-hopelessly-fancy-rhino
01'
