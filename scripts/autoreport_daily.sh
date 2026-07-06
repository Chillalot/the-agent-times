#!/bin/bash
# Master Pipeline: Phase 1 → Collect ALL data, Phase 2 → Write ALL articles
# Chạy vào 8h sáng mỗi ngày, đồng bộ tất cả hạng mục

SCRIPTS_DIR="$HOME/.hermes/profiles/meow/scripts"
REPORTS_DIR="$HOME/.hermes/profiles/meow/reports"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "═══════════════════════════════════════════════"
echo "  📡 MASTER PIPELINE — $TIMESTAMP"
echo "  PHASE 1: THU THẬP DỮ LIỆU"
echo "═══════════════════════════════════════════════"
echo ""

# === PHASE 1: COLLECT ALL RAW DATA ===
echo "📰 [1/5] Daily Briefing (RSS VN)..."
python3 daily_briefing.py > /tmp/phase1_daily.txt 2>/dev/null
echo "   ✅ Done"

echo "💻 [2/5] Tech News..."
python3 tech_news.py > /tmp/phase1_tech.txt 2>/dev/null
echo "   ✅ Done"

echo "🐙 [3/5] GitHub Radar..."
python3 github_radar.py > /tmp/phase1_github.txt 2>/dev/null
echo "   ✅ Done"

echo "🌍 [4/5] International News..."
python3 international_news.py > /tmp/phase1_intl.txt 2>/dev/null
echo "   ✅ Done"

echo "🍗 [5/5] F&B Report..."
python3 fnb_market_report.py > /tmp/phase1_fnb.txt 2>/dev/null
echo "   ✅ Done"

echo ""
echo "═══════════════════════════════════════════════"
echo "  PHASE 2: VIẾT ARTICLES"
echo "═══════════════════════════════════════════════"
echo ""

# === PHASE 2: WRITE ALL ARTICLES ===
echo "📝 [1/5] Scrape VN articles from RSS URLs..."
URLS=$(cat /tmp/phase1_daily.txt | grep -oP 'https?://vnexpress\.net/[^\s"'"'"'()<>,\]]+' | sort -u)
echo "   Found $(echo "$URLS" | grep -c . 2>/dev/null || echo 0) URLs"
COUNT=0
while IFS= read -r url; do
  [ -z "$url" ] && continue
  cat="economy"
  case "$url" in
    *kinh-doanh*|*kinh-te*|*gdp*|*startup*) cat="economic" ;;
    *thue*|*phap-luat*|*quy-dinh*) cat="legal" ;;
    *so-hoa*|*cong-nghe*|*khoa-hoc*) cat="technology" ;;
    *doi-song*) cat="fnb" ;;
  esac
  python3 article_scraper.py "$url" "$cat" > /dev/null 2>&1 && COUNT=$((COUNT+1))
done <<< "$URLS"
echo "   ✅ $COUNT articles written"

echo "🐙 [2/5] GitHub articles..."
python3 github_article_writer.py 2>&1 | grep "✅\|⏭️"

echo "📊 [3/5] Legal/Tax guide..."
python3 legal_tax_guide.py > /dev/null 2>&1
echo "   ✅ Done"

echo "🍗 [4/5] F&B report..."
python3 run_and_save.py fnb_market_report.py fnb "🍗 F&B & Quán ăn" > /dev/null 2>&1
echo "   ✅ Done"

echo "🌍 [5/5] International articles (via RSS + translate)..."
echo "   (handled by international_news.py already)"

echo ""
echo "═══════════════════════════════════════════════"
echo "  📊 TỔNG KẾT"
echo "═══════════════════════════════════════════════"
echo ""
for cat in economy technology github legal affiliate fnb economic; do
  N=$(ls $REPORTS_DIR/*.json 2>/dev/null | while read f; do python3 -c "import json; d=json.load(open('$f')); print(d.get('category',''))" 2>/dev/null; done | grep -c "^$cat$" || echo 0)
  echo "  $(printf '%-15s' $cat): $N articles"
done
echo ""
echo "📁 Total: $(ls $REPORTS_DIR/*.json 2>/dev/null | wc -l) files"
echo "═══════════════════════════════════════════════"

rm -f /tmp/phase1_*.txt
