#!/usr/bin/env python3
"""
Legal & Tax Research Tool — F&B Edition (mở rộng)
Cho Long - từ quán cơm gà → tổng thể F&B
Bao gồm: hộ KD cá thể, Công ty TNHH, chuỗi, franchise, cloud kitchen
"""

import json
from datetime import datetime

INFO = {
    "loai_hinh": {
        "title": "CÁC LOẠI HÌNH KINH DOANH F&B TẠI VIỆT NAM",
        "source": "Luật Doanh nghiệp 2014/2020, Wikipedia",
        "details": """
┌─────────────────────────────────────────────────────────────┐
│ 1️⃣  HỘ KINH DOANH CÁ THỂ — cho quán đơn lẻ, quy mô nhỏ      │
├─────────────────────────────────────────────────────────────┤
• 1 cá nhân hoặc nhóm người/hộ gia đình làm chủ
• Dưới 10 lao động
• Chỉ đăng ký tại 1 địa điểm duy nhất
• Không có con dấu pháp nhân
• Chịu trách nhiệm vô hạn bằng tài sản cá nhân
• Không được phát hành hóa đơn GTGT (dùng hóa đơn bán lẻ)
• ✅ Phù hợp: quán cơm gà, quán ăn vặt, take-away nhỏ

┌─────────────────────────────────────────────────────────────┐
│ 2️⃣  CÔNG TY TNHH / CÔNG TY CỔ PHẦN — cho chuỗi, quy mô lớn  │
├─────────────────────────────────────────────────────────────┤
• Từ 2 thành viên trở lên (TNHH 2TV) hoặc 1 (TNHH 1TV)
• Đăng ký tại Sở KHĐT tỉnh/thành phố
• Vốn điều lệ: không tối thiểu (tùy ngành, nhưng nên ≥ 100tr)
• Có con dấu pháp nhân
• Chịu trách nhiệm hữu hạn trong vốn góp
• Được xuất hóa đơn GTGT, khấu trừ thuế đầu vào
• Chi phí thành lập: ~3-10 triệu (tự làm) hoặc 5-15tr (dịch vụ)
• ✅ Phù hợp: mở >1 quán, có chuỗi, cần gọi vốn

┌─────────────────────────────────────────────────────────────┐
│ 3️⃣  MÔ HÌNH CHUỖI / FRANCHISE                              │
├─────────────────────────────────────────────────────────────┤
• Khi mở quán thứ 2 trở đi: cần cân nhắc lên Công ty TNHH
• Franchise (nhượng quyền): cần đăng ký theo NĐ 35/2006
  - Thương hiệu đã vận hành tối thiểu 1 năm
  - Có hệ thống vận hành chuẩn (SOP)
  - Đăng ký tại Bộ Công Thương nếu nhượng quyền từ nước ngoài
• Hợp tác kinh doanh (góp vốn): cần hợp đồng hợp tác rõ ràng
  - Phân chia lợi nhuận, trách nhiệm, rủi ro
  - Nên có luật sư soạn thảo
• ✅ Phù hợp: nhân rộng mô hình quán cơm gà thành chuỗi
"""
    },
    "giay_phep": {
        "title": "GIẤY TỜ & THỦ TỤC CHO QUÁN ĂN / F&B",
        "source": "Luật ATTP 2010, NĐ 15/2018, NĐ 155/2018",
        "details": """
═══ BẮT BUỘC ═══

1️⃣ Đăng ký hộ kinh doanh cá thể / Giấy CN ĐKKD
   • UBND quận/huyện nơi đặt quán
   • Hồ sơ: CMND/CCCD, đơn đăng ký, hợp đồng thuê mặt bằng (nếu có)
   • Thời gian: 3-5 ngày
   • Lệ phí: 100-200k

2️⃣ Giấy chứng nhận ATVS thực phẩm (ATTP)
   • Ban Quản lý ATTP cấp tỉnh/thành phố
   • Hồ sơ: Giấy phép KD, sơ đồ cơ sở, bản cam kết ATTP,
     giấy khám sức khỏe, giấy tập huấn ATTP
   • Thời gian: 15-20 ngày
   • Lệ phí: ~500k-1tr
   • ⚠️ Miễn nếu chỉ kinh doanh thực phẩm bao gói sẵn
   • Quán chế biến trực tiếp: BẮT BUỘC phải có

3️⃣ Mã số thuế
   • Chi cục Thuế quận/huyện
   • Làm cùng lúc với đăng ký hộ KD

4️⃣ Giấy khám sức khỏe (chủ + nhân viên)
   • Bệnh viện quận/huyện
   • Hiệu lực 12 tháng
   • ~100-200k/người

5️⃣ Tập huấn kiến thức ATTP
   • Chi cục ATTP
   • ~200-500k/người

═══ THEO MÔ HÌNH ═══

🍗 Quán cơm gà nhỏ (hộ KD): Giấy tờ #1 → #5
☕ Trà sữa / cf nhỏ: Giấy tờ #1 → #5
🏪 Chuỗi >1 quán: Công ty TNHH + #2 → #5 cho từng cơ sở
🏭 Cloud Kitchen: #1/#2 → #5 + PCCC (nếu >200m²)
🛵 Take-away chỉ: Có thể chỉ cần #1 + #3 (nếu bán mang đi đơn giản)

═══ KHUYẾN KHÍCH ═══
• Bảng hiệu quảng cáo (thông báo UBND nếu ≥20m²)
• Hợp đồng lao động với nhân viên
• Đăng ký PCCC nếu diện tích >200m² hoặc trên 1 tầng
"""
    },
    "thue": {
        "title": "THUẾ CHO HỘ KD & DOANH NGHIỆP F&B",
        "source": "Thông tư 92/2015/TT-BTC, NĐ 139/2016, NĐ 22/2020",
        "details": f"""
═══ PHẦN 1: HỘ KINH DOANH CÁ THỂ (quán nhỏ) ═══

1️⃣  THUẾ MÔN BÀI (Lệ phí môn bài)
   • Doanh thu ≤ 100 triệu/năm: MIỄN
   • 100-300 triệu: 300.000đ/năm
   • 300-500 triệu: 500.000đ/năm
   • > 500 triệu: 1.000.000đ/năm
   • Miễn năm đầu

2️⃣  THUẾ GTGT: 1% × Doanh thu

3️⃣  THUẾ TNCN: 1.5% × Doanh thu

💰 TỔNG THUẾ KHOÁN: 2.5% × Doanh thu
   Ví dụ: Doanh thu 30tr/tháng → thuế ~750k/tháng

═══ PHẦN 2: CÔNG TY TNHH (chuỗi/quy mô lớn) ═══

1️⃣  THUẾ TNDN: 20% × Lợi nhuận (Doanh thu - Chi phí)
   • Chi phí hợp lý: nguyên liệu, nhân công, thuê mặt bằng, khấu hao...
   • Được khấu trừ thuế GTGT đầu vào
   • Cần hóa đơn đầu vào đầy đủ

2️⃣  THUẾ GTGT: 10% (khấu trừ: thuế đầu ra - thuế đầu vào)
   • Nếu doanh thu < 1 tỷ/năm: có thể chọn nộp theo tỷ lệ % (khoán)

3️⃣  THUẾ MÔN BÀI:
   • Vốn điều lệ ≤ 10 tỷ: 2.000.000đ/năm
   • Vốn điều lệ > 10 tỷ: 3.000.000đ/năm

═══ SO SÁNH NHANH ═══
┌──────────────────────┬──────────┬─────────────┐
│ Khoản mục            │ Hộ KD    │ Cty TNHH    │
├──────────────────────┼──────────┼─────────────┤
│ Thuế tổng cộng       │ ~2.5% DT │ 20% LN      │
│ Được khấu trừ đầu vào│ ❌       │ ✅           │
│ Phù hợp khi          │ <1 quán  │ >1 quán     │
│ Trách nhiệm          │ Vô hạn   │ Hữu hạn     │
│ Chi phí thành lập    │ ~200k    │ ~5-15tr     │
│ Kế toán              │ Tự làm   │ DV ~500k-1tr│
└──────────────────────┴──────────┴─────────────┘
"""
    },
    "nghi_dinh_moi": {
        "title": "CÁC NGHỊ ĐỊNH MỚI CẦN THEO DÕI (2024-2025)",
        "source": "Tổng hợp từ báo chí & thuvienphapluat.vn",
        "details": """
═══ LUẬT & NGHỊ ĐỊNH LIÊN QUAN F&B ═══

📜 Luật An toàn thực phẩm 2010 (sửa đổi 2018)
• NĐ 15/2018/NĐ-CP: Quy định chi tiết ATTP
• NĐ 155/2018/NĐ-CP: Xử phạt vi phạm ATTP
  - Phạt đến 50 triệu cho vi phạm về điều kiện bảo quản
  - Phạt đến 100 triệu cho vi phạm về sử dụng hóa chất cấm

📜 Luật Doanh nghiệp 2020
• Nới lỏng thủ tục đăng ký
• Cho phép hộ KD chuyển đổi lên doanh nghiệp

📜 Thuế
• NĐ 22/2020: Sửa đổi thuế môn bài (miễn giảm cho hộ nhỏ)
• NĐ 139/2016: Quy định lệ phí môn bài

📜 Lao động
• Bộ luật Lao động 2019
• Hợp đồng lao động: bắt buộc nếu có nhân viên
• Mức lương tối thiểu vùng (2025): ~4.9-5.3tr/tháng

═══ CẬP NHẬT MỚI NHẤT từ báo chí ═══
• Chính phủ tiếp tục giảm thuế xăng dầu
• Đề xuất giảm thuế GTGT cho một số ngành dịch vụ (có thể gồm F&B)

⚠️ LƯU Ý KHI MỞ RỘNG CHUỖI:
• Mỗi quán thêm → cần thêm giấy phép ATTP riêng
• Nếu nhượng quyền: cần đăng ký franchise
• Hợp tác với đối tác: cần hợp đồng hợp tác có công chứng
• Nên nhờ luật sư/kế toán tư vấn trước khi mở rộng
"""
    },
    "cost_estimate": {
        "title": "DỰ TOÁN CHI PHÍ — CÁC MÔ HÌNH F&B",
        "source": "Tham khảo thị trường Việt Nam 2024-2025",
        "details": """
════════════════════════════════════════════════════
 MÔ HÌNH 1: QUÁN CƠM GÀ NHỎ (hộ KD, mặt bằng nhà)
════════════════════════════════════════════════════
📦 Đăng ký giấy tờ:          1.000.000 - 2.000.000đ
🪑 Bàn ghế (5-7 bộ):        5.000.000 - 15.000.000đ
🍳 Bếp + nồi niêu:           5.000.000 - 10.000.000đ
🥘 Tô chén muỗng đũa:        2.000.000 - 5.000.000đ
💡 Trang trí + bảng hiệu:    3.000.000 - 10.000.000đ
🛒 Tủ lạnh:                  5.000.000 - 15.000.000đ
🔥 Bếp gas/hồng ngoại:       3.000.000 - 8.000.000đ
───────────────────────────────────────────────
💰 TỔNG VỐN:               ~26.000.000 - 65.000.000đ
  • Điểm hòa vốn: 30-35 suất/ngày
  • Lợi nhuận mục tiêu: 20-30%

════════════════════════════════════════════════════
 MÔ HÌNH 2: QUÁN CƠM GÀ + THUÊ MẶT BẰNG
════════════════════════════════════════════════════
💰 Vốn đầu tư:              ~40.000.000 - 90.000.000đ
  (Phần chi phí ban đầu ~26-65tr + cọc mặt bằng 2-3 tháng)
  
Chi phí vận hành tháng:
🏠 Mặt bằng:                 5.000.000 - 15.000.000đ
🐔 Nguyên liệu:             15.000.000 - 30.000.000đ
⚡ Điện nước:                 2.000.000 - 5.000.000đ
👨‍🍳 Nhân công:                6.000.000 - 12.000.000đ
💰 Thuế:                       500.000 - 2.000.000đ
📦 Phát sinh:                 1.000.000 - 3.000.000đ
───────────────────────────────────────────────
📊 DOANH THU CẦN ĐẠT:
  • Giá suất: 35.000 - 55.000đ
  • Hòa vốn: 40-50 suất/ngày (tùy mặt bằng)
  • Với 50 suất/ngày → Doanh thu ~55-82tr/tháng

════════════════════════════════════════════════════
 MÔ HÌNH 3: CHUỖI 2-3 QUÁN (Công ty TNHH)
════════════════════════════════════════════════════
💰 Vốn mở rộng: Quán đầu ~70tr, quán tiếp ~50-60tr
  (Tiết kiệm nhờ đã có thương hiệu, quy trình)

Chi phí phát sinh khi mở rộng:
• Quản lý + kế toán:           3.000.000 - 5.000.000đ/tháng
• Xây dựng quy trình (SOP):    10.000.000 - 20.000.000đ (one-time)
• Phần mềm quản lý:            500.000 - 2.000.000đ/tháng
• Marketing:                    2.000.000 - 5.000.000đ/tháng

📈 KINH NGHIỆM:
• Chỉ nhân rộng khi quán đầu đã ổn định >6 tháng
• Lợi thế quy mô: mua nguyên liệu số lượng lớn → giá rẻ hơn
• Rủi ro: loãng quản lý, giảm chất lượng

════════════════════════════════════════════════════
 MÔ HÌNH KHÁC (THAM KHẢO NHANH)
════════════════════════════════════════════════════
🥤 Trà sữa nhỏ: Vốn 30-80tr, biên lợi nhuận 60-75%
☕ Cà phê đặc sản: Vốn 50-200tr, cần concept mạnh
🥗 Ăn vặt healthy: Vốn 20-50tr, đang là xu hướng mới
🏭 Cloud Kitchen: Vốn 30-80tr, tiết kiệm mặt bằng 50%
🛵 Take-away: Vốn 15-30tr, cần tối ưu giao hàng
"""
    }
}

def print_section(key, data):
    print(f"\n{'=' * 60}")
    print(f"📋  {data['title']}")
    print(f"📎  Nguồn: {data['source']}")
    print(f"{'=' * 60}")
    print(data["details"])

def main():
    print(f"\n{'█' * 60}")
    print(f"  ⚖️  CẨM NANG PHÁP LÝ & THUẾ — F&B TỔNG THỂ")
    print(f"  Cho Long 🍗 | Cập nhật: {datetime.now().strftime('%d/%m/%Y')}")
    print(f"{'█' * 60}")
    
    sections = ["loai_hinh", "giay_phep", "thue", "nghi_dinh_moi", "cost_estimate"]
    for s in sections:
        print_section(s, INFO[s])
    
    print(f"\n{'=' * 60}")
    print("🔥 TIP CHO LONG: MỞ RỘNG TỪ QUÁN CƠM GÀ")
    print(f"{'=' * 60}")
    print("""
  • 🍗 Bắt đầu: quán cơm gà (hộ KD cá thể) — học vận hành
  • 📊 Ghi chép số liệu 6 tháng — hiểu chi phí, doanh thu, lợi nhuận
  • 👨‍🍳 Đào tạo nhân sự — để có thể ủy thác
  • 📝 Xây dựng SOP (quy trình chuẩn) — cho từng món, từng công đoạn
  • 🏪 Mở quán thứ 2 — lên Công ty TNHH
  • 🔗 Tính đến franchise/chuỗi — khi đã có thương hiệu

  💡 "Làm nhỏ mà chỉnh chu còn hơn làm lớn mà cẩu thả" 🚀
    """)
    print(f"\n{'=' * 60}")
    print("⚠️  DISCLAIMER: Thông tin mang tính tham khảo.")
    print("   Luôn kiểm tra với cơ quan chức năng địa phương")
    print("   và tham vấn luật sư/kế toán để có thông tin chính xác nhất.")

if __name__ == "__main__":
    main()
