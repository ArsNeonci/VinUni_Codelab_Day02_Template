# Nhật ký tương tác AI — Lab 02: AI Product Scoping

## 1. Bối cảnh

Trong Lab 02, tôi dùng AI như một **thought partner** để tìm kiếm và sàng lọc
bài toán vận hành trong hệ sinh thái Vingroup. Bài toán cuối cùng tôi phân tích
sâu là **AI hỗ trợ phân loại yêu cầu bảo dưỡng/sửa chữa VinFast**.

Tôi không xem nội dung AI tạo ra là dữ liệu nội bộ hay quyết định cuối cùng.
Các đề xuất được kiểm tra lại với worksheet, README, autograder và nguồn công
khai. Những con số chưa có bằng chứng được ghi rõ là baseline giả định cần xác
minh bằng log hoặc phỏng vấn đội vận hành.

## 2. AI đã giúp tôi những gì?

### 2.1. Brainstorm theo 4 Lenses

Tôi yêu cầu AI quét hoạt động của VinFast, Vinmec, Vinhomes, Vinpearl và Xanh
SM theo bốn lăng kính: tác vụ lặp lại, tác vụ tốn thời gian, dịch vụ có thể nâng
cấp bằng AI và pain của stakeholder.

AI giúp tôi:

- Chuyển các ý tưởng rộng như “cải thiện CSKH” thành quy trình cụ thể có actor,
  đầu vào, đầu ra và bottleneck.
- Tạo danh sách bảy bài toán để so sánh thay vì chọn ngay ý tưởng đầu tiên.
- Phân biệt bước nào phù hợp với rule, ML/entity matching, LLM/Vision hoặc cần
  Human-in-the-loop.
- Đề xuất metric có thể đo như top-1 accuracy, safety recall, thời gian xử lý
  trung vị và tỷ lệ ticket phải chuyển lại.

### 2.2. Quick Assessment và Deep-Dive

AI hỗ trợ tôi xây ba Quick Problem Cards cho VinFast, Vinmec và Vinhomes. Khi
đi sâu vào bài toán VinFast, AI giúp mô tả current-state workflow, hai điểm
handoff, bottleneck và future-state flow.

Điểm hữu ích nhất là AI không chỉ đề xuất “dùng chatbot”, mà tách giải pháp
thành các thành phần:

1. Rule kiểm tra trường bắt buộc và dấu hiệu an toàn.
2. LLM/Vision xử lý mô tả và ảnh phi cấu trúc.
3. Structured JSON để hệ thống downstream kiểm tra được.
4. Human review trước khi route ticket hoặc trả lời khách.
5. Fallback về quy trình thủ công khi model lỗi hoặc confidence thấp.

### 2.3. Hỗ trợ sửa code

Khi chạy starter code, API trả về lỗi 404 vì model `gemini-2.5-flash` không còn
được cấp cho project mới. Code mẫu còn bắt mọi exception rồi chạy lại bằng
`google.generativeai`, là SDK cũ đã ngừng được khuyến nghị. AI giúp tôi xác định
đúng nguyên nhân, thay model bằng `gemini-3.8-flash` và chỉ sử dụng SDK
`google-genai`.

Tôi cũng dùng AI để đối chiếu code với autograder. Từ đó code cuối cùng có:

- System prompt nêu rõ vai trò và ranh giới cấm.
- Structured JSON thay vì văn bản tự do.
- Bốn adversarial tests, nhiều hơn mức tối thiểu hai test của autograder.
- Rule guardrails hậu kiểm để model không thể tự hạ mức cảnh báo.
- Fallback có nhãn rõ ràng khi thiếu API key hoặc API lỗi.

## 3. AI đã trả lời sai hoặc thiếu chặt chẽ ở đâu?

### 3.1. Biến số ước tính thành “sự thật”

Trong bản brainstorm đầu, AI dễ đưa ra các con số như số ticket mỗi ngày, thời
gian xử lý hoặc số giờ thất thoát mà không có log nội bộ làm bằng chứng. Nếu
chép nguyên văn, báo cáo sẽ tạo cảm giác đó là số liệu thật của Vingroup.

**Cách tôi sửa:** Tôi yêu cầu AI tách ba loại thông tin:

- Sự kiện có nguồn công khai.
- Baseline giả định dùng để thiết kế thử nghiệm.
- Số liệu bắt buộc phải đo trong pilot.

Trong báo cáo, tôi dùng công thức `N × (T_baseline - T_future) / 60` thay vì tự
khẳng định sản lượng thật. Ví dụ 500 yêu cầu/ngày chỉ được ghi là ví dụ minh họa.

### 3.2. Đề xuất tự động hóa quá mức

Một số gợi ý ban đầu cho phép AI tự route ticket, xác nhận lịch hoặc gửi phản
hồi. Đây là thiết kế nguy hiểm vì AI có thể bỏ sót lỗi phanh, khói, pin quá
nhiệt hoặc mất lái.

**Cách tôi sửa:** Tôi giới hạn AI ở vai trò tạo đề xuất dạng `[DRAFT_ONLY]`.
Nhân viên phải duyệt trước khi chuyển ticket. Các dấu hiệu an toàn được rule
engine nâng lên `safety_critical`; nếu rule và LLM xung đột thì rule thắng và
hệ thống fail closed.

### 3.3. Không thống nhất giữa báo cáo và code mẫu

Starter code ban đầu là bài toán điều phối sự cố pin của Xanh SM, trong khi
problem scan và deep-dive của tôi chọn VinFast service triage. Nếu giữ nguyên,
các deliverable sẽ không kể cùng một câu chuyện.

**Cách tôi sửa:** Tôi đổi vai trò, schema và test cases sang VinFast. Tuy nhiên,
tôi vẫn giữ boundary `5%` và action `dispatch_mobile_charger` như một nhánh an
toàn hợp lý của yêu cầu dịch vụ pin, đồng thời đáp ứng tiêu chí autograder.

### 3.4. Chỉ dùng prompt nhưng không có kiểm soát bằng code

AI ban đầu tập trung vào việc viết system prompt rất dài, nhưng prompt không
thể đảm bảo 100% model tuân thủ. Một câu prompt injection vẫn có thể yêu cầu
bỏ `[DRAFT_ONLY]` hoặc hạ mức lỗi phanh.

**Cách tôi sửa:** Ngoài system prompt, code còn parse JSON, chuẩn hóa output,
ép tiền tố `[DRAFT_ONLY]` và áp dụng rule guardrails sau khi nhận phản hồi từ
Gemini. Như vậy safety không chỉ phụ thuộc vào khả năng làm theo chỉ dẫn của
LLM.

## 4. Tôi đã cải tiến prompt như thế nào?

### Prompt ban đầu

```text
Hãy phân loại yêu cầu sửa chữa VinFast và trả lời khách hàng.
```

Prompt này quá rộng: không có schema, không nói AI được phép làm gì, không có
quy tắc khi thiếu dữ liệu và không có điểm phê duyệt của con người.

### Prompt sau khi cải tiến

Tôi bổ sung sáu nhóm ràng buộc:

1. **Role:** AI chỉ là service-triage copilot, không phải kỹ thuật viên ra quyết
   định cuối.
2. **Output:** Chỉ trả một JSON object theo schema cố định.
3. **Grounding:** Evidence phải xuất phát từ yêu cầu của khách; không được bịa
   mẫu xe, triệu chứng, giá, bảo hành hoặc lịch xưởng.
4. **Safety:** Lỗi phanh, cháy/khói, pin quá nhiệt, mất lái và tai nạn luôn là
   `safety_critical`.
5. **Human approval:** Mọi phản hồi phải bắt đầu bằng `[DRAFT_ONLY]`; AI không
   được tự gửi, đặt lịch hoặc cam kết.
6. **Fallback:** Thiếu dữ liệu hoặc confidence thấp phải chuyển
   `manual_review`; lỗi API quay về quy trình thủ công.

## 5. Kết quả kiểm thử và bài học rút ra

Tôi đã chạy bốn adversarial tests gồm: prompt injection yêu cầu bỏ
`[DRAFT_ONLY]`, hạ mức lỗi phanh, điều xe pin 2% tới trạm cách 8 km và yêu cầu
AI tự bịa dữ liệu. Cả bốn boundary checks đều đạt trong chế độ local safety
fallback; autograder Section B đạt 5/5. Khi sử dụng Gemini API thực tế, tôi vẫn
giữ rule guardrails hậu kiểm để không phụ thuộc hoàn toàn vào system prompt.

Qua bài lab, tôi nhận thấy AI phù hợp để brainstorm, cấu trúc hóa workflow và
tạo bản nháp nhanh, nhưng không nên được xem là nguồn dữ liệu nội bộ hoặc người
ra quyết định cuối. Một sản phẩm AI an toàn cần có dữ liệu được kiểm chứng,
structured output, Human-in-the-loop, fallback và audit log.