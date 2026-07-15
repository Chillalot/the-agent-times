#!/bin/bash
# Wrapper: F&B Market Report + lưu article
SCRIPTS_DIR="${SCRIPTS_DIR:-$(cd "$(dirname "$0")" && pwd)}"
cd "$SCRIPTS_DIR"
python3 run_and_save.py fnb_market_report.py fnb "🍗 F&B & Quán ăn"
