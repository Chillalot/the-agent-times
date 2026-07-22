#!/bin/bash
# Pipeline: International News → Translate → Save
SCRIPTS_DIR="${SCRIPTS_DIR:-$(cd "$(dirname "$0")" && pwd)}"
REPORTS_DIR="${REPORTS_DIR:-$(dirname "$SCRIPTS_DIR")/data/reports}"
cd "$SCRIPTS_DIR"

echo "🌍 Pipeline International News"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
timeout 300 python3 international_news.py 2>&1 | grep "📄\|✅\|❌\|📊\|🌐"
echo ""
echo "✅ Done! Articles: $(ls $REPORTS_DIR/intl_*.json 2>/dev/null | wc -l)"
