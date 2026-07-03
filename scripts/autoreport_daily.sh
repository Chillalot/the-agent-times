#!/bin/bash
# ================================================================
# Pipeline: Daily Briefing → Article Scraper → Save
# Chạy báo cáo hàng ngày + tự động scrape từng link thành bài báo
# KHÔNG xuất raw link list — chỉ xuất articles đã scrape
# ================================================================

SCRIPTS_DIR="$HOME/.hermes/profiles/meow/scripts"
REPORTS_DIR="$HOME/.hermes/profiles/meow/reports"

cd "$SCRIPTS_DIR"

echo "📡 Pipeline báo cáo & Article Scraper"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Bước 1: Chạy Daily Briefing (thu thập URLs)
echo "📰 Thu thập dữ liệu..."
python3 daily_briefing.py > /tmp/daily_briefing_output.txt 2>/dev/null
BRIEFING_OUT=$(cat /tmp/daily_briefing_output.txt)

# Bước 2: Trích xuất URLs
URLS=$(echo "$BRIEFING_OUT" | grep -oP 'https?://vnexpress\.net/[^\s"'"'"'()<>,\]]+' | sort -u)
URL_COUNT=$(echo "$URLS" | grep -c . 2>/dev/null || echo 0)
echo "   Tìm thấy $URL_COUNT URLs"

# Bước 3: Scrape từng URL → article
SUCCESS=0
FAIL=0
while IFS= read -r url; do
  [ -z "$url" ] && continue
  cat="daily-briefing"
  case "$url" in
    *kinh-doanh*|*kinh-te*|*gdp*|*startup*) cat="economic" ;;
    *thue*|*phap-luat*|*quy-dinh*) cat="legal" ;;
    *so-hoa*|*cong-nghe*|*khoa-hoc*) cat="github" ;;
    *doi-song*|*an-choi*|*am-thuc*) cat="fnb" ;;
  esac
  RESULT=$(python3 article_scraper.py "$url" "$cat" 2>&1)
  if echo "$RESULT" | grep -q "✅"; then
    TITLE=$(echo "$RESULT" | grep "✅ Đã lưu" | sed 's/✅ Đã lưu: //')
    echo "   📰 $TITLE"
    SUCCESS=$((SUCCESS + 1))
  else
    FAIL=$((FAIL + 1))
  fi
done <<< "$URLS"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ $SUCCESS articles mới / $FAIL lỗi"
echo "📁 Tổng: $(ls $REPORTS_DIR/article_*.json 2>/dev/null | wc -l) articles"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

rm -f /tmp/daily_briefing_output.txt
