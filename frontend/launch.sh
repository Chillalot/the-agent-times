#!/bin/bash
# ================================================================
#  Phương's Daily — NYT Newspaper Launcher
#  Khởi động server, mở trình duyệt, tự dọn dẹp khi đóng tab
# ================================================================

PORT=5050
FRONTEND_DIR="$HOME/.hermes/profiles/meow/frontend"
LOG_FILE="$FRONTEND_DIR/server.log"
MARKER="$FRONTEND_DIR/.launched"

# Kill server cũ nếu còn
lsof -ti:$PORT 2>/dev/null | xargs kill 2>/dev/null

cd "$FRONTEND_DIR"

# Xác định Python
PYTHON=$(command -v python3)
[ -z "$PYTHON" ] && PYTHON=$(command -v python)

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║     📡  Phương's Daily              ║"
echo "  ║     Báo cáo Kinh tế & Công nghệ     ║"
echo "  ╠══════════════════════════════════════╣"
echo "  ║  🌐 http://localhost:$PORT             ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  🚀 Đang khởi động server..."

# Start server trong background
$PYTHON app.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Đợi server sẵn sàng (tối đa 10 giây)
for i in $(seq 1 10); do
    if curl -s "http://localhost:$PORT" > /dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

echo "  ✅ Server đã sẵn sàng (PID: $SERVER_PID)"
echo ""

# Mở trình duyệt
if command -v xdg-open &>/dev/null; then
    xdg-open "http://localhost:$PORT" 2>/dev/null &
elif command -v open &>/dev/null; then
    open "http://localhost:$PORT" 2>/dev/null &
else
    echo "  ⚠️  Không mở được trình duyệt tự động"
    echo "  👉 Hãy mở: http://localhost:$PORT"
fi

echo "  ─────────────────────────────────────────"
echo "  📖  Server đang chạy..."
echo "  🛑  Nhấn ENTER hoặc Ctrl+C để dừng server"
echo "  ─────────────────────────────────────────"
echo ""

# Chờ user input
read -r

# Cleanup
echo "  🛑 Đang dọn dẹp..."
kill $SERVER_PID 2>/dev/null
rm -f "$MARKER"

# Gọi shutdown endpoint để đảm bảo cleanup
curl -s "http://localhost:$PORT/shutdown" > /dev/null 2>&1

echo "  ✅ Server đã dừng. Hẹn gặp lại!"
echo ""
