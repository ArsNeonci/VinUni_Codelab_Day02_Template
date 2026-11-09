# 01 — Problem Scan & Quick Cards (Vinmec)

> **Tác giả:** manhcuong · **Mảng:** 🏥 Vinmec — Y tế thông minh
>
> **Quy ước số liệu:** `[N]` = có nguồn (xem cuối file) · `[GĐ]` = giả định của tác giả, **cần đo lại tại Vinmec** trước khi dùng để ra quyết định. Bài tập dùng nghiên cứu tài liệu công khai, không có dữ liệu nội bộ Vinmec.

---

## 🔍 Phase 1 — SCAN

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | **Vinmec** | Tốn thời gian | Bác sĩ điều trị soạn **bản tóm tắt hồ sơ bệnh án khi ra viện** thủ công: đọc lại ghi chú nhiều ngày, chép kết quả xét nghiệm, thuốc, viết lời dặn. Ước tính 15–30 phút/bản `[N1]`; giấy tờ chiếm ~47% thời gian làm thủ tục ra viện `[N2]`. |
| 2 | **Vinmec** | Pain từ người khác | Khách đặt lịch qua tổng đài/app **chọn sai chuyên khoa** (VD: đau ngực → Tiêu hóa thay vì Tim mạch), phải chuyển khoa, chờ lại, khiếu nại. |
| 3 | **Vinmec** | Lặp lại | Nhân viên **kiểm tra hồ sơ bảo lãnh viện phí** bảo hiểm tư nhân: đối chiếu giấy tờ, mã bệnh, quyền lợi — thao tác giống nhau mỗi ca, chậm làm bệnh nhân chờ lúc ra viện `[N3]`. |
| 4 | **Vinmec** | AI có thể tốt hơn | Bệnh nhân hỏi **ý nghĩa kết quả xét nghiệm** trên app/tổng đài, nhận câu trả lời rập khuôn "vui lòng hỏi bác sĩ" → gọi lại nhiều lần. |
| 5 | **Vinmec** | Lặp lại | Điều dưỡng/CSKH **gọi điện nhắc lịch tái khám** thủ công; bệnh nhân bỏ hẹn (no-show) gây trống lịch bác sĩ. |
| 6 | **Vinmec** | Lặp lại | **Mã hóa chẩn đoán ICD-10** từ chẩn đoán viết tự do để làm hồ sơ thanh toán BHYT/bảo hiểm; mã sai → bị xuất toán, phải làm lại. |

**Lọc nhanh trước khi làm thẻ** — câu hỏi đầu tiên luôn là *"có cần AI không?"*:
- #5 nhắc lịch: lịch hẹn đã có cấu trúc → **SMS/Zalo tự động theo rule** là đủ. Giữ lại làm thẻ để minh họa "No AI".
- #4 giải thích xét nghiệm: rủi ro tư vấn y khoa trực tiếp cho bệnh nhân, ranh giới khó giữ → loại ở vòng này.
- #6 ICD-10: đáng làm nhưng cần dữ liệu mã hóa lịch sử để đánh giá → để sau.

---

## 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

### Card #1 — Tóm tắt hồ sơ bệnh án khi ra viện

```text
┌───────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                         │
│                                                               │
│ Bài toán: Bác sĩ mất 15–30 phút/bệnh nhân để soạn bản tóm tắt │
│ hồ sơ bệnh án khi ra viện, phần lớn là chép lại dữ liệu đã có │
│ sẵn trong bệnh án điện tử.                                    │
│ Công ty thành viên: [x] Vinmec                                │
│                                                               │
│ Ai đang đau? Bác sĩ điều trị (quá tải giấy tờ cuối ca).       │
│ Người bệnh chỉ đau gián tiếp.                                 │
│                                                               │
│ Workflow thủ công hiện tại:                                   │
│  1. Khám cuối, quyết định ra viện                             │
│  → 2. Mở bệnh án điện tử, đọc lại ghi chú điều trị nhiều ngày │
│  → 3. Chép chẩn đoán, kết quả CLS, thuốc vào mẫu tóm tắt      │
│  → 4. Viết diễn biến điều trị + lời dặn cho người bệnh        │
│  → 5. Chuyển trưởng khoa ký                                   │
│                                                               │
│ Bước tốn nhất? Bước 2–4 (⏱ ~20 phút/bản [GĐ], khớp 15–30 [N1])│
│ AI nhảy vào đâu?                                              │
│  - Bước 3: KHÔNG cần AI → template tự điền từ dữ liệu có cấu  │
│    trúc (chẩn đoán, thuốc, xét nghiệm).                       │
│  - Bước 4: LLM soạn NHÁP diễn biến + lời dặn dễ hiểu.         │
│                                                               │
│ Metric:                                                       │
│  - Thời gian bác sĩ trên 1 bản (đo bằng log bệnh án điện tử): │
│    ~20 phút ──> ≤ 12 phút                                     │
│  - 0 sai lệch thuốc/liều so với đơn ra viện                   │
│                                                               │
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent   │
│ (Template + LLM feature hẹp, bác sĩ duyệt bắt buộc)           │
└───────────────────────────────────────────────────────────────┘
```

**Tự phản biện (vai CFO/Trưởng phòng Vận hành khó tính):**
1. *"Bác sĩ nói tiết kiệm 10 phút nhưng thực đo được bao nhiêu?"* — Đúng là rủi ro: pilot Stanford ghi nhận bác sĩ **cảm thấy** tiết kiệm >10 phút nhưng log bệnh án điện tử chỉ thấy **~3 phút** `[N1]`. → Metric bắt buộc đo bằng log, không bằng khảo sát.
2. *"LLM bịa thì ai chịu?"* — Nghiên cứu GPT-4 cho thấy 42% bản tóm tắt có hallucination, 47% bỏ sót `[N4]`. → Không để LLM viết phần dữ liệu (thuốc, xét nghiệm); phần đó dùng template.
3. *"Template thôi có đủ không?"* — Có thể phần lớn giá trị nằm ở template. → Đây chính là lý do triển khai template trước, đo, rồi mới quyết định có cần LLM.

---

### Card #2 — Gợi ý chuyên khoa khi đặt lịch khám

```text
┌───────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                         │
│                                                               │
│ Bài toán: Khách tự chọn chuyên khoa khi đặt lịch, chọn sai    │
│ → chuyển khoa, chờ lại, tốn slot bác sĩ.                      │
│ Công ty thành viên: [x] Vinmec                                │
│                                                               │
│ Ai đang đau? Khách hàng, tổng đài viên, bác sĩ nhận sai ca.   │
│                                                               │
│ Workflow thủ công hiện tại:                                   │
│  1. Khách gọi tổng đài / mở app                               │
│  → 2. Mô tả triệu chứng                                       │
│  → 3. Tổng đài viên đoán chuyên khoa theo kinh nghiệm         │
│  → 4. Xếp lịch → đến khám → (nếu sai) chuyển khoa             │
│                                                               │
│ Bước tốn nhất? Bước 3 (⏱ ~3–5 phút/cuộc [GĐ]) + chi phí chuyển │
│ khoa khi sai.                                                 │
│ AI nhảy vào đâu? Bước 3: gợi ý top-2 chuyên khoa từ mô tả.    │
│                                                               │
│ Metric: Tỉ lệ chuyển khoa do đặt sai: ~10% [GĐ] ──> < 5%      │
│                                                               │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent   │
└───────────────────────────────────────────────────────────────┘
```

**Tự phản biện:**
1. Chưa có baseline "tỉ lệ đặt sai khoa" — con số 10% là giả định.
2. Rủi ro an toàn: triệu chứng cấp cứu (đau ngực, khó thở) **không được** đi qua luồng đặt lịch thường. Phần này cần **rule cứng** (từ khóa đỏ → chuyển cấp cứu), LLM không được quyết định.
3. Cây câu hỏi rule-based (form chọn vùng cơ thể + triệu chứng) có thể giải quyết phần lớn mà không cần LLM.

---

### Card #5 — Nhắc lịch tái khám (thẻ "No AI")

```text
┌───────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #5                                         │
│                                                               │
│ Bài toán: Điều dưỡng/CSKH gọi điện nhắc tái khám thủ công;    │
│ bệnh nhân vẫn bỏ hẹn.                                         │
│ Công ty thành viên: [x] Vinmec                                │
│                                                               │
│ Ai đang đau? CSKH (gọi lặp lại), bác sĩ (lịch trống).         │
│                                                               │
│ Workflow thủ công hiện tại:                                   │
│  1. Xuất danh sách hẹn ngày mai                               │
│  → 2. Gọi từng người                                          │
│  → 3. Ghi xác nhận / dời lịch                                 │
│                                                               │
│ Bước tốn nhất? Bước 2 (⏱ ~2 phút/cuộc [GĐ])                   │
│ AI nhảy vào đâu? KHÔNG CẦN. Lịch hẹn đã có cấu trúc.          │
│ Giải pháp: SMS/Zalo tự động T-1 ngày + nút xác nhận/dời lịch; │
│ chỉ gọi người chưa xác nhận.                                  │
│                                                               │
│ Metric: Số cuộc gọi thủ công/ngày giảm ≥ 70%;                 │
│         tỉ lệ no-show (đo baseline trước) giảm.               │
│                                                               │
│ Quick Architecture: [x] No AI  [x] Rule  [ ] LLM  [ ] Agent   │
└───────────────────────────────────────────────────────────────┘
```

**Tự phản biện:** đây là ví dụ cho nguyên tắc *Problem first, AI second*: thêm LLM vào đây chỉ tăng chi phí và rủi ro mà không giải quyết thêm vấn đề nào.

---

## 🗳️ Đề xuất chọn bài để Deep-Dive

**Chọn Card #1 — Tóm tắt hồ sơ bệnh án khi ra viện.**

| Card | Quyết định | Lý do |
|---|---|---|
| #1 Tóm tắt ra viện | ✅ Chọn | Gánh nặng có số liệu từ nghiên cứu `[N1][N2]`; dữ liệu đầu vào đã có trong bệnh án điện tử; ranh giới rõ (bác sĩ ký duyệt); có thể bắt đầu bằng template không cần AI. |
| #2 Gợi ý chuyên khoa | ⏸ Để sau | Chưa có baseline; rủi ro an toàn với ca cấp cứu; nên thử cây câu hỏi rule-based trước. |
| #5 Nhắc tái khám | ❌ Không cần AI | Rule + SMS giải quyết được; chuyển cho team vận hành làm ngay. |

**Lưu ý quan trọng từ nghiên cứu nghiệp vụ:** thời gian **người bệnh chờ** ra viện chủ yếu do khâu thanh toán/giám định bảo hiểm `[N3]`, không phải khâu soạn tóm tắt. Vì vậy Card #1 **không** hứa "bệnh nhân về sớm hơn"; mục tiêu là **giảm tải cho bác sĩ** và giữ chất lượng hồ sơ.

---

## 📚 Nguồn

- `[N1]` Stanford Medicine (2026) — AI discharge summary pilot: https://med.stanford.edu/news/all-news/2026/06/ai-discharge-summary.html · tóm tắt: https://www.pulse.bot/healthtech/news/stanfords-ai-discharge-summary-tool-cuts-physician-burnout-7a6e6627-61b1-4db3-83f0-332e4aeb0e17/
- `[N2]` Time-motion study ra viện, khoa Nội tổng quát (Toronto) — trích qua kết quả tìm kiếm; cần đọc bản gốc để trích dẫn chính thức.
- `[N3]` BV Nhi Đồng — cải tiến thời gian chờ xuất viện (2019): https://nhidong.org.vn/data/bvnhidong\bvnhidong\attachments/2019_9/hoinghinhikhoa2019/47_ttxv_tam_hoinghi2019_21920199.pdf
- `[N4]` Williams et al. — LLMs drafting ED discharge summaries: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11023681/
