# User Workflow Patterns — Làm việc với Long

## ⚠️ CẤM Code Mù — Quy trình BẮT BUỘC

### Vấn đề
Trong session ngày 03/07/2026, user đã nhiều lần nói "có thay đổi gì đâu" dù file đã sửa. Lý do:
- Mình code xong → báo "done" → user không thấy gì trên browser
- Mình dispatch subagent → báo "xong" → user vẫn không thấy thay đổi
- Mình chỉ CSS variables mà không restructure HTML templates

### Rule #1: Plan → Approve → Build → Verify

```
[Research] → [Viết Plan chi tiết] → [User duyệt] → [Build từng Phase] → [User verify] → [Next Phase]
```

Mỗi Phase phải có:
- **Definition of Done** rõ ràng (có thể đo đếm được)
- **User phải verify** trước khi qua phase tiếp theo
- **Không nói "done"** khi user chưa xác nhận trên browser của họ

### Rule #2: Chia subagent NHỎ — mỗi đứa 1 việc

```
✅ ĐÚNG:                          ❌ SAI:
Agent 1: Extract HTML structure   Agent: "Rewrite the whole CSS"
Agent 2: Extract CSS rules        
Agent 3: Rewrite templates        
```

- Mỗi subagent = 1 task cụ thể, có input file + output file rõ ràng
- Task quá broad → split thành 2-3 subagent nhỏ hơn
- Max 3 subagent concurrent (giới hạn Hermes)

### Rule #3: Verify trên browser của USER, không chỉ curl

- `curl -s http://localhost:5050/ | grep ...` — chỉ check nội bộ
- User dùng **Cốc Cốc browser** — cần test thực tế trên browser đó
- Nếu user nói "không thấy gì" → khả năng: (a) server không chạy, (b) cache, (c) bind sai IP

### Rule #4: Server Infrastructure Checklist

Trước khi báo "server ready", verify:
- [ ] Server bind 0.0.0.0 (không phải 127.0.0.1)
- [ ] Cache headers: `no-cache, no-store, must-revalidate`
- [ ] CSS cache busting: `style.css?v={{ random }}`
- [ ] Server chạy background — không kill
- [ ] User có thể access từ Cốc Cốc: `http://localhost:5050` hoặc `http://<IP>:5050`

### Rule #5: Design change phải visible ngay

Khi sửa design, user phải thấy KHÁC ngay lập tức:
- [ ] Accent color thay đổi (header, button, link — 3 places minimum)
- [ ] Font thay đổi (headline, body, UI — 3 levels)
- [ ] Layout thay đổi (header structure, hero, cards, footer)
- [ ] Spacing thay đổi (gap, padding, margin)
- [ ] Dark mode khác biệt rõ

Nếu bất kỳ item nào chưa khác → chưa xong → quay lại code.

### Rule #6: Clone website = Copy CẢ HTML + CSS

```
✅ Clone đúng:                         ❌ Clone sai:
1. Extract HTML structure (templates)   1. Chỉ extract color palette
2. Extract CSS rules (style.css)        2. Chỉ đổi CSS variables
3. Apply both → restart → verify        3. Không sửa templates
```

CSS variables ALONE không đủ để clone design. Cần restructure templates (thêm section mới, đổi class names) + components CSS (BEM classes như .image-box, .post-card, .subnav).

## Ponytail Philosophy cho Workflow

> "The best code is the code you never wrote. The best plan prevents wasting code."

- **Tại sao viết plan?** Vì viết code mất 10x thời gian hơn viết plan. Sai plan thì sửa dễ, sai code thì sửa 10x.
- **Tại sao subagent nhỏ?** Vì subagent lớn dễ miss context, output quality thấp. 3 task nhỏ = 3 file output rõ ràng.
- **Tại sao verify sớm?** Vì phát hiện lỗi càng muộn, fixed càng đắt (cost of change curve).
