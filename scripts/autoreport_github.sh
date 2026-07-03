#!/bin/bash
# Pipeline: GitHub Radar → Article Writer
SCRIPTS_DIR="$HOME/.hermes/profiles/meow/scripts"
REPORTS_DIR="$HOME/.hermes/profiles/meow/reports"

cd "$SCRIPTS_DIR"
echo "🐙 Pipeline GitHub Radar"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"

# Bước 1: GitHub Radar (thu thập repo data)
echo "📡 Thu thập repo trending..."
python3 github_radar.py > /tmp/github_output.txt 2>/dev/null

# Bước 2: Lưu raw data
python3 run_and_save.py github_radar.py github "🐙 Công nghệ & GitHub" > /dev/null 2>&1

# Bước 3: GitHub Article Writer → mỗi repo = 1 bài báo
echo "✍️ Viết articles cho từng repo..."
if [ -f "github_article_writer.py" ]; then
  python3 github_article_writer.py 2>&1 | grep "✅\|⏭️" | while read line; do
    echo "   $line"
  done
fi

echo ""
echo "✅ Hoàn tất! $(ls $REPORTS_DIR/article_*.json $REPORTS_DIR/github_article_*.json 2>/dev/null | wc -l) articles"
rm -f /tmp/github_output.txt
