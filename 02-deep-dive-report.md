# 02 — Deep-Dive Report
**Tên nhóm:** A95
**Thành viên:**
- Trương Thị Thu Hà — 26ai.hattt@vinuni.edu.vn
- <Họ tên thành viên 2> — <email>
- <Họ tên thành viên 3> — <email>

**Bài toán nhóm chọn:** ...
**Vì sao chọn / vì sao loại các bài khác:** ...

## 3.1. Current-State Workflow
Sơ đồ: xem file `04-workflow-diagram.png`
1. <Bước> — Ai: ... — ⏱ ... phút
2. <Bước> — Ai: ... — ⏱ ... phút 🔄 (bàn giao cho ...)
3. <Bước> — Ai: ... — ⏱ ... phút 🔴 (bottleneck)
4. ...

**Tổng cộng = ... phút/lượt**

## 3.2. Problem Statement (6-field)
| Field | Nội dung |
|---|---|
| 1. Actor / Operator | |
| 2. Current Workflow | |
| 3. Bottleneck | |
| 4. Business Impact | (thời gian, chi phí, SLA — có số) |
| 5. Success Metric | (ví dụ: giảm từ 15 phút xuống dưới 3 phút) |
| 6. Operational Boundary | AI được làm: ... / TUYỆT ĐỐI KHÔNG: ... / Điểm cần người duyệt: ... |

## 3.3. Future-State Flow & AI Fit
| Mức | Phương án | Đủ khi nào | Rủi ro | Chọn? |
|---|---|---|---|---|
| Rule / State-Machine | | | | |
| LLM Feature | | | | |
| Agentic Loop | | | | |

**Future-State Flow:**
1. ... → 2. 🔵 AI: ... → 3. 🟢 Người duyệt: ... → 4. ...

↩️ **Fallback:** nếu AI trả về lỗi hoặc không chắc chắn thì ...

## Phase 4 — Kết quả Prompt Prototype
- Ranh giới đã test: [DRAFT_ONLY] bắt buộc ở đầu tin nháp; pin dưới 5% thì không chỉ trạm sạc xa hơn 5km mà điều xe sạc di động.
- Kết quả: ... / 3 test Passed

## Phase 5 — Evaluate
- [ ] Có sẵn dữ liệu mẫu / logs sạch để test?
- [ ] Rủi ro khi AI sai nằm trong tầm kiểm soát (HITL / Fallback)?
- [ ] Stakeholders sẵn sàng thay đổi quy trình cũ?

**Quyết định:** GO / NOT YET / NO-GO
**Justification:** ...
