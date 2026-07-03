---
name: vietnam-business-regulations
description: "Hướng dẫn pháp lý, thuế, giấy phép cho hộ kinh doanh cá thể và doanh nghiệp F&B tại Việt Nam. Cho Long 🍗"
version: 2.0.0
author: Phương
tags: [vietnam, business, legal, tax, regulations, F&B, small-business, chain]
---

# Vietnam Business Regulations (F&B Edition)

## Khi nào dùng skill này?
- Khi cần tra cứu thủ tục, giấy phép, thuế cho quán ăn / F&B
- Khi muốn so sánh hộ KD cá thể vs Công ty TNHH để mở rộng
- Khi cần dự toán chi phí mở quán / mở chuỗi
- Khi tìm hiểu về franchise / nhượng quyền F&B

## Reference files
- `references/taxes-permits-detailed.md` — Knowledge bank đầy đủ: thuế, giấy phép, quy trình, kinh nghiệm thực tế

## Phương pháp Research (cho agent)
Khi cần tra cứu luật/thuế Việt Nam:
1. **Wikipedia API (ưu tiên):** `vi.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=<title>&format=json`
   - Hoạt động tốt, không bị Cloudflare chặn
   - Các title hay dùng: `Hộ_kinh_doanh_cá_thể`, `Thuế_Việt_Nam`, `Công_ty_trách_nhiệm_hữu_hạn`
2. **RSS feeds báo chí** — VnExpress RSS hoạt động không Cloudflare
3. **Tránh** thuvienphapluat.vn, luatminhkhue.vn — bị Cloudflare chặn nặng

## Nội dung chính

### 1. Hộ kinh doanh cá thể (Quán nhỏ, 1 địa điểm)
- 1 người/nhóm/hộ gia đình làm chủ
- Dưới 10 lao động
- 1 địa điểm đăng ký
- Chịu trách nhiệm vô hạn bằng tài sản cá nhân
- ✅ Phù hợp: quán cơm gà, quán ăn vặt, take-away nhỏ

### 2. Công ty TNHH (Chuỗi, >1 quán)
- Đăng ký tại Sở KHĐT tỉnh/thành phố
- Chịu trách nhiệm hữu hạn trong vốn góp
- Được xuất hóa đơn GTGT, khấu trừ thuế đầu vào
- Chi phí thành lập: ~5-15tr (dịch vụ)
- ✅ Phù hợp: mở >1 quán, có chuỗi, cần gọi vốn

### 3. Giấy tờ bắt buộc (quán ăn)
1. Đăng ký hộ KD / Giấy CN ĐKKD (UBND quận/huyện, ~3-5 ngày)
2. Giấy ATVSTP (Ban QL ATTP, ~15-20 ngày) — **BẮT BUỘC** nếu chế biến trực tiếp
3. Mã số thuế (Chi cục Thuế)
4. Giấy khám sức khỏe (chủ + nhân viên, 12 tháng)
5. Tập huấn ATTP

### 4. Thuế
| Loại hình | Thuế suất |
|-----------|----------|
| Hộ KD (quán nhỏ) | ~2.5% doanh thu (khoán) |
| Hộ KD (doanh thu <100tr/năm) | MIỄN THUẾ |
| Công ty TNHH | 20% lợi nhuận |
| Thuế môn bài (hộ KD) | Miễn đến 500k-1tr/năm |

### 5. Mở rộng chuỗi - Lưu ý pháp lý
- Quán thứ 2 trở đi → cần lên Công ty TNHH
- Mỗi cơ sở cần giấy ATTP riêng
- Nếu nhượng quyền → đăng ký franchise (NĐ 35/2006)
- Hợp tác với đối tác → hợp đồng hợp tác công chứng

## Hệ thống báo cáo & Frontend

Hệ thống báo cáo tự động đã được xây dựng, giao diện phong cách NYT:
- **🌐 Web:** `http://localhost:5050`
- **🚀 Khởi động:** Nhấp đúp icon `Phương's Daily 📡` trên Desktop (hoặc `launch.sh`)
- **⏰ Cronjob:** Báo cáo mới tự động xuất hiện 8h sáng mỗi ngày
- **📂 Reports:** `~/.hermes/profiles/meow/reports/` (JSON)

### Xem báo cáo
1. Mở trình duyệt → http://localhost:5050
2. Chọn ngày bằng date picker / ◀ Ngày trước / Ngày sau ▶
3. Lọc danh mục: Kinh tế, Công nghệ, Pháp lý, F&B
4. Tìm kiếm toàn bộ bài viết

### Scripts chạy thủ công
- `python3 ~/.hermes/profiles/meow/scripts/legal_tax_guide.py`
- `python3 ~/.hermes/profiles/meow/scripts/daily_briefing.py`
- `python3 ~/.hermes/profiles/meow/scripts/github_radar.py`
- `python3 ~/.hermes/profiles/meow/scripts/fnb_market_report.py`

## Lưu ý
- Luôn kiểm tra với Chi cục Thuế địa phương
- Nên nhờ kế toán dịch vụ khi mở rộng (~500k-1tr/tháng)
- Xem thêm skill `vietnam-fnb-market-analysis` — phân tích chi phí & thị trường
- Xem thêm skill `fnb-chain-management` — quản lý chuỗi F&B
- Xem thêm skill `news-web-design` — thiết kế frontend báo cáo
