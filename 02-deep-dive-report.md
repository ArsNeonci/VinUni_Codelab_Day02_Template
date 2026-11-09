# Báo cáo Phân tích sâu — AI hỗ trợ phân loại yêu cầu dịch vụ VinFast

## Tóm tắt lựa chọn

Bài toán được chọn từ [01-problem-scan.md](01-problem-scan.md) là **Card #1 —
VinFast phân loại yêu cầu bảo dưỡng/sửa chữa**.

Mục tiêu của dự án là hỗ trợ cố vấn dịch vụ đọc nội dung và ảnh do khách hàng
gửi, trích xuất triệu chứng, đề xuất nhóm dịch vụ, mức ưu tiên và nơi xử lý phù
hợp. AI chỉ tạo **đề xuất dạng nháp**; nhân viên VinFast giữ quyền xác nhận,
sửa hoặc từ chối trước khi yêu cầu được chuyển tới xưởng hay đội Mobile
Service.

> **Giả định cần xác minh:** Các mốc thời gian và sản lượng trong báo cáo là
> baseline phục vụ thiết kế thử nghiệm, không phải số liệu vận hành nội bộ đã
> được VinFast xác nhận.

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping

### Quy trình hiện tại giả định

```text
┌──────────────────────┐
│ Bước 1               │
│ Khách gửi yêu cầu,   │
│ thông tin xe và ảnh  │
│ ⏱ 0,5–1 phút         │
└──────────┬───────────┘
           │ 🔄 Handoff: App/Web/Hotline → CSKH
           ▼
┌──────────────────────┐
│ Bước 2               │
│ Kiểm tra thông tin   │
│ có đầy đủ hay không  │
│ ⏱ 1–2 phút           │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Bước 3 🔴            │
│ Đọc mô tả, xem ảnh,  │
│ nhận diện triệu chứng│
│ ⏱ 3–5 phút           │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Bước 4 🔴            │
│ Chọn nhóm dịch vụ,   │
│ mức ưu tiên, nơi xử lý│
│ ⏱ 2–3 phút           │
└──────────┬───────────┘
           │ 🔄 Handoff: CSKH → Xưởng/Mobile Service
           ▼
┌──────────────────────┐
│ Bước 5               │
│ Chuyển yêu cầu và    │
│ phản hồi khách hàng  │
│ ⏱ 1,5–3 phút         │
└──────────────────────┘
```

- **Tổng thời gian xử lý giả định:** khoảng **8–14 phút/yêu cầu**.
- **Bottleneck chính:** Bước 3 và 4, chiếm khoảng **5–8 phút/yêu cầu**.
- **Điểm dễ lỗi:** mô tả tự do, ảnh mờ, một yêu cầu có nhiều triệu chứng,
  nhầm giữa sửa chữa tại xưởng và Mobile Service, hoặc đánh giá thiếu mức độ
  khẩn cấp.
- **Hệ quả:** yêu cầu có thể bị chuyển sai đội, phải phân loại lại, làm tăng
  thời gian xác nhận lịch và thời gian chờ của khách hàng.

### Dữ liệu đầu vào và đầu ra hiện tại

| Thành phần | Nội dung |
|---|---|
| **Đầu vào** | Họ tên/SĐT, mẫu xe, biển số, số km, nội dung yêu cầu, nhóm dịch vụ khách tự chọn, địa điểm, thời gian và tối đa các ảnh hiện trạng. |
| **Công cụ** | App/website/hotline, hệ thống ticket, danh mục dịch vụ và lịch của xưởng. |
| **Đầu ra** | Category dịch vụ, mức ưu tiên, xưởng hoặc Mobile Service, yêu cầu bổ sung thông tin và phản hồi xác nhận cho khách. |
| **Người chịu trách nhiệm** | Nhân viên CSKH/cố vấn dịch vụ; xưởng hoặc đội Mobile Service xác nhận khả năng tiếp nhận. |

## 3.2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên CSKH và cố vấn dịch vụ VinFast là người đọc, phân loại và chuyển yêu cầu. Xưởng dịch vụ hoặc đội Mobile Service là bên tiếp nhận. Khách hàng là stakeholder chịu ảnh hưởng trực tiếp bởi thời gian xác nhận và độ chính xác của việc phân luồng. |
| **2. Current Workflow** | Khách gửi thông tin xe, mô tả và ảnh qua kênh số hoặc hotline. Nhân viên kiểm tra dữ liệu, đọc mô tả/xem ảnh, đối chiếu danh mục, xác định mức ưu tiên và nơi xử lý, sau đó chuyển ticket để xác nhận lịch và phản hồi khách. Quy trình giả định gồm 5 bước, mất khoảng 8–14 phút/yêu cầu. |
| **3. Bottleneck** | Bước đọc–hiểu mô tả/ảnh và quyết định category, priority, destination mất khoảng 5–8 phút. Ngôn ngữ của khách không chuẩn hóa, ảnh có thể thiếu ngữ cảnh, và các dấu hiệu an toàn như lỗi phanh, khói, pin quá nhiệt hoặc mất lái không được phép bị bỏ sót. |
| **4. Business Impact** | Gọi **N** là số yêu cầu/ngày. Nếu AI giúp tiết kiệm trung bình 6 phút/yêu cầu, năng lực tiết kiệm tiềm năng là `N × 6 / 60 = 0,1N giờ công/ngày`. Ví dụ minh họa, không phải số liệu VinFast: tại 500 yêu cầu/ngày, tiềm năng là 50 giờ công/ngày. Lợi ích khác gồm giảm chuyển sai đội, giảm rework và rút ngắn thời gian khách nhận xác nhận. |
| **5. Success Metric** | (a) Top-1 category accuracy ≥ **85%**; (b) top-3 accuracy ≥ **95%**; (c) recall đối với yêu cầu an toàn nghiêm trọng ≥ **99%**, đồng thời **0 trường hợp** bị AI tự hạ mức ưu tiên mà không qua người duyệt; (d) thời gian phân loại trung vị dưới **60 giây**; (e) giảm ít nhất **50%** tỷ lệ ticket phải chuyển lại giữa các đội so với baseline; (f) 100% đề xuất và hành động duyệt/sửa được ghi audit log. |
| **6. Operational Boundary** | AI được phép trích xuất dữ liệu, đề xuất category/priority/destination, chỉ ra thông tin còn thiếu và soạn phản hồi dạng `[DRAFT_ONLY]`. AI **không được** tự chẩn đoán kỹ thuật, báo giá, cam kết thời gian hoàn thành, tự xác nhận lịch, tự hạ mức khẩn cấp hoặc tự gửi phản hồi. Ticket confidence thấp, dữ liệu mâu thuẫn hoặc có dấu hiệu an toàn phải chuyển người xử lý. |

### Giả thuyết giá trị cần kiểm chứng

> Nếu hệ thống AI đa phương thức có thể đề xuất đúng nhóm dịch vụ trong top-1
> tối thiểu 85% và phát hiện tối thiểu 99% trường hợp có dấu hiệu an toàn, thì
> thời gian phân loại trung vị có thể giảm từ baseline 3–5 phút xuống dưới 60
> giây mà không làm tăng tỷ lệ phân luồng sai.

## 3.3. Future-State Flow & AI Fit

### Lựa chọn AI Fit

- [ ] **Rule / State-Machine thuần túy**
- [x] **LLM Feature + Computer Vision, có rule guardrails**
- [ ] **Agentic Loop tự trị**

**Lý do:** Rule phù hợp để bắt các điều kiện rõ như từ khóa an toàn, trường bắt
buộc và mapping category–đội xử lý. Tuy nhiên, rule thuần túy khó xử lý cách mô
tả đa dạng, lỗi chính tả và ảnh hiện trạng. LLM/Vision phù hợp để trích xuất và
phân loại dữ liệu phi cấu trúc. Agent tự trị không cần thiết vì quy trình ngắn,
đích đến hữu hạn và quyết định sai có thể ảnh hưởng an toàn; con người phải giữ
quyền phê duyệt.

### Structured Output đề xuất

```json
{
  "request_id": "string",
  "vehicle_model": "string_or_unknown",
  "symptoms": ["string"],
  "service_category": "enum",
  "severity": "normal|urgent|safety_critical",
  "evidence": ["text_or_image_observation"],
  "missing_fields": ["string"],
  "recommended_destination": "workshop|mobile_service|roadside_assistance|manual_review",
  "confidence": 0.0,
  "draft_reply": "[DRAFT_ONLY] ..."
}
```

### Future-State Workflow

```text
┌──────────────────────┐
│ Khách gửi form + ảnh │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 🔵 Rule validation   │
│ Kiểm tra trường bắt  │
│ buộc, loại file      │
│ ⏱ < 5 giây           │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 🔵 AI multimodal     │
│ Trích xuất + đề xuất │
│ JSON có evidence     │
│ ⏱ mục tiêu < 20 giây│
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 🔵 Safety guardrail  │
│ Rule kiểm tra mức    │
│ khẩn cấp/confidence  │
└───────┬───────┬──────┘
        │       │
   Bình thường  │ Safety-critical/low confidence
        │       └───────────────────────────┐
        ▼                                   ▼
┌──────────────────────┐        ┌──────────────────────┐
│ 🟢 HITL: Nhân viên   │        │ 🟢 Hàng đợi ưu tiên │
│ duyệt/sửa đề xuất    │        │ Chuyên viên xử lý   │
│ ⏱ mục tiêu < 60 giây│        │ thủ công ngay       │
└──────────┬───────────┘        └──────────┬───────────┘
           │                               │
           └───────────────┬───────────────┘
                           ▼
                ┌──────────────────────┐
                │ Chuyển xưởng/đội    │
                │ dịch vụ và gửi phản │
                │ hồi đã được duyệt   │
                └──────────────────────┘
```

### Cơ chế Human-in-the-loop

| Tình huống | Hành động của AI | Hành động bắt buộc của con người |
|---|---|---|
| Đủ dữ liệu, confidence cao, không có dấu hiệu an toàn | Hiển thị category, evidence, destination và draft reply | Nhân viên đọc, duyệt hoặc sửa trước khi chuyển ticket. |
| Confidence thấp hoặc nhiều category cạnh tranh | Đánh dấu `manual_review`, nêu thông tin còn thiếu | Nhân viên yêu cầu khách bổ sung hoặc tự phân loại. |
| Có dấu hiệu phanh, khói, pin quá nhiệt, mất lái hoặc tai nạn | Rule nâng lên `safety_critical`; AI không được hạ mức | Nhân viên ưu tiên kiểm tra và quyết định điều phối cứu hộ/xưởng. |
| AI đề xuất khác với lựa chọn của nhân viên | Lưu cả đề xuất và lý do/evidence | Nhân viên ghi category đúng; dữ liệu được đưa vào tập đánh giá sau khi kiểm duyệt. |

### Fallback

| Sự cố | Fallback |
|---|---|
| API/LLM không phản hồi hoặc timeout | Đưa ticket về hàng đợi thủ công hiện tại; không làm mất dữ liệu khách đã gửi. |
| Ảnh hỏng, mờ hoặc định dạng không hỗ trợ | Bỏ qua suy luận từ ảnh, đánh dấu thiếu dữ liệu và yêu cầu ảnh mới; không bịa nội dung ảnh. |
| JSON sai schema | Validator từ chối output và thử lại tối đa một lần; nếu vẫn lỗi thì chuyển thủ công. |
| Confidence dưới ngưỡng | Không tự route; chuyển `manual_review`. Ngưỡng được hiệu chỉnh bằng tập validation, không đặt tùy ý khi production. |
| AI và safety rule xung đột | **Fail closed:** safety rule thắng, ticket được nâng ưu tiên và chuyển người xử lý. |
| Phát hiện dữ liệu cá nhân ngoài phạm vi | Che/mã hóa trường nhạy cảm, chặn log prompt thô và báo quản trị hệ thống. |

### Kiến trúc logic tối thiểu

```text
App/Web/Hotline
      │
      ▼
Schema validation + PII controls
      │
      ├── Rule engine: trường bắt buộc và safety keywords
      │
      ▼
Multimodal model: text + image → structured JSON
      │
      ▼
Output validator + confidence policy
      │
      ▼
Human Review UI → Ticket System → Workshop/Mobile Service
      │
      └── Audit log + feedback labels
```

## 3.4. Kế hoạch dữ liệu và đánh giá

### Dữ liệu tối thiểu cho prototype offline

1. Tối thiểu **1.000 yêu cầu lịch sử đã ẩn danh**, có đủ mô tả và ảnh hợp lệ
   nếu được phép sử dụng.
2. Danh mục category, severity và destination thống nhất giữa CSKH và xưởng.
3. Mỗi mẫu được ít nhất một chuyên gia gán nhãn; tối thiểu 20% mẫu được hai
   chuyên gia gán độc lập để đo độ nhất quán.
4. Tách train/dev/test theo thời gian hoặc request ID để tránh cùng một sự cố
   xuất hiện ở nhiều tập.
5. Tập safety riêng chứa các tình huống phanh, khói, pin quá nhiệt, mất lái,
   tai nạn, ảnh mờ và prompt injection trong nội dung khách hàng.

### Thiết kế thử nghiệm

- **Baseline 1:** Nhân viên xử lý theo quy trình hiện tại.
- **Baseline 2:** Bộ rule/từ khóa không dùng LLM.
- **Candidate:** LLM/Vision + rule guardrails + HITL.
- Đánh giá accuracy theo từng category, precision/recall của
  `safety_critical`, thời gian xử lý trung vị/P90, tỷ lệ nhân viên chấp nhận
  đề xuất và tỷ lệ ticket phải chuyển lại.
- Không triển khai production nếu recall safety-critical dưới 99% hoặc xuất
  hiện trường hợp AI tự hạ mức cảnh báo mà không qua người duyệt.

---

# 🏁 Phase 5 — EVALUATE

## 5.1. AI Readiness Checklist

| Tiêu chí | Trạng thái | Bằng chứng/việc còn thiếu |
|---|---|---|
| Có sẵn dữ liệu mẫu/log sạch để test | [ ] **Chưa xác nhận** | Public form cho thấy có dữ liệu đầu vào số hóa, nhưng nhóm chưa được cung cấp log lịch sử, nhãn chuẩn, quyền sử dụng ảnh và thống kê phân bố category. |
| Rủi ro khi AI sai nằm trong tầm kiểm soát | [x] **Có điều kiện** | Có HITL, rule an toàn, confidence threshold, audit log và fallback thủ công. Tuy nhiên phải stress-test trên tập safety trước pilot. |
| Stakeholders sẵn sàng thay đổi quy trình | [ ] **Chưa xác nhận** | Chưa phỏng vấn CSKH, cố vấn dịch vụ, quản lý xưởng và đội Mobile Service; chưa đo thời gian baseline hoặc mức chấp nhận đề xuất. |

### Checklist mở rộng

| Hạng mục | Trạng thái | Điều kiện đạt |
|---|---|---|
| Problem–AI fit | [x] | Có dữ liệu phi cấu trúc dạng text/ảnh; rule thuần túy khó bao phủ cách mô tả đa dạng. |
| Metric | [x] | Có ngưỡng accuracy, safety recall, latency, re-route và auditability. |
| Privacy & access control | [ ] | Cần xác định data retention, masking, quyền xem ảnh/biển số/SĐT và vùng lưu trữ dữ liệu. |
| Integration | [ ] | Chưa xác nhận API của ticket system, lịch xưởng và Mobile Service. |
| Fallback | [x] | Có thể quay về hàng đợi thủ công hiện tại khi AI lỗi hoặc confidence thấp. |
| Owner vận hành | [ ] | Cần chỉ định Product Owner, Data Owner và người chịu trách nhiệm duyệt thay đổi category taxonomy. |

## 5.2. Quyết định

- [ ] **GO — bắt đầu triển khai production**
- [x] **NOT YET — chuẩn bị dữ liệu và xác lập baseline trước**
- [ ] **NO-GO — hủy bài toán**

### Justification

Bài toán có AI fit hợp lý vì đầu vào gồm mô tả tự do và ảnh, trong khi output
là tập category hữu hạn có thể kiểm tra. Rủi ro cũng có thể giới hạn bằng rule
an toàn, structured output, Human-in-the-loop và fallback thủ công. Vì vậy đây
**không phải NO-GO**.

Tuy nhiên, hiện chưa có bằng chứng rằng nhóm đã sở hữu dữ liệu lịch sử đủ sạch,
nhãn category thống nhất, quyền sử dụng ảnh khách hàng, baseline thời gian hoặc
sự đồng thuận của nhân viên vận hành. Chọn GO ngay sẽ biến các mục tiêu 85%,
95% và 99% thành giả định không thể kiểm chứng. Vì vậy quyết định phù hợp là
**NOT YET cho triển khai thực tế**, đồng thời cho phép thực hiện prototype
offline sau khi hoàn thành các cổng dữ liệu tối thiểu.

## 5.3. Điều kiện chuyển từ NOT YET sang GO

1. Thu thập và ẩn danh tối thiểu 1.000 yêu cầu, có taxonomy và nhãn được đội
   nghiệp vụ phê duyệt.
2. Đo baseline tối thiểu hai tuần: thời gian phân loại, tỷ lệ chuyển sai, tỷ lệ
   thiếu dữ liệu và sản lượng theo ngày/category.
3. Hoàn tất đánh giá privacy/security cho mô tả, ảnh, biển số và số điện thoại.
4. Prototype offline đạt top-1 ≥ 85%, top-3 ≥ 95%, safety recall ≥ 99% và không
   có trường hợp tự hạ mức cảnh báo.
5. Pilot shadow mode: AI chỉ gợi ý, không ảnh hưởng workflow thật; so sánh với
   quyết định của nhân viên.
6. Pilot có kiểm soát trên tối đa 10% lưu lượng trong hai tuần, có nút tắt và
   rollback ngay lập tức.
7. CSKH, quản lý xưởng, Data Owner và Security cùng ký duyệt trước khi mở rộng.

## 5.4. Ước lượng chi phí và lợi ích

Do chưa có đơn giá nhân sự và giá inference nội bộ, báo cáo dùng công thức để
tránh tạo số liệu tài chính giả:

### Chi phí prototype

```text
C_prototype
= 20 ngày-công AI Engineer × C_AI/ngày
+ 10 ngày-công Backend Engineer × C_BE/ngày
+ 5 ngày-công Domain Expert × C_SME/ngày
+ 5 ngày-công QA/Security × C_QA/ngày
+ Chi phí inference, storage và monitoring trong thử nghiệm
```

### Lợi ích vận hành tiềm năng

```text
Giờ công tiết kiệm/ngày = N × (T_baseline - T_future) / 60

Giá trị tiết kiệm/tháng
= Giờ công tiết kiệm/ngày × C_nhân_sự/giờ × Số ngày vận hành
+ Giá trị giảm rework/chuyển sai
+ Giá trị giảm thời gian khách chờ
```

Với giả định minh họa `T_baseline = 8 phút`, `T_future = 2 phút`, phần tiết
kiệm là `0,1N giờ/ngày`. Nhóm chỉ được tính ROI và thời gian hòa vốn sau khi có
**N**, chi phí nhân sự, chi phí inference và tỷ lệ rework thực đo.
