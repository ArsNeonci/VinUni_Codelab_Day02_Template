# 03 — AI Log & Reflection

> **Tác giả:** manhcuong · **Công cụ AI:** Claude Code (Claude Opus 5.5) — dùng làm thought-partner và trợ lý code trong suốt lab.
>
> Phần **Nhật ký** ghi lại sự kiện thật trong phiên làm việc. Phần **Phản ánh cá nhân** do tôi tự viết.

---

## 1. Nhật ký tương tác (sự kiện thật)

| # | Tôi yêu cầu / quyết định | AI làm gì | Kết quả |
|---|---|---|---|
| 1 | Đọc toàn bộ đề, tóm tắt nhiệm vụ cá nhân; "không làm gì khi chưa cho phép" | Đọc README, worksheet, ví dụ, inspiration kit, **và cả `autograder.py`** | Phát hiện autograder chấm code bằng cách dò từ khóa của bài Xanh SM — thông tin không có trong README. |
| 2 | Chọn Vinmec; yêu cầu tư duy PM thực dụng: baseline → điểm nghẽn → giải pháp đơn giản | AI đề xuất bài "tóm tắt xuất viện", hướng template + LLM | Hướng đi tốt, nhưng **AI nhảy thẳng vào giải pháp trước khi hiểu nghiệp vụ** (xem lỗi #A). |
| 3 | **Tôi hỏi: "có cần bước tìm hiểu nghiệp vụ không?"** | AI đồng ý, thêm Bước 0 có giới hạn thời gian và tiêu chí quyết định | Bước này thay đổi cả cách đặt bài toán (xem #5). |
| 4 | Hỏi rõ tiêu chí 1 của autograder; chất vấn "vậy khác gì ép chọn Xanh SM?" | AI giải thích cơ chế dò từ khóa, thừa nhận đề bài tự mâu thuẫn, đưa 3 phương án | **Tôi quyết định** làm Vinmec trọn vẹn, chấp nhận mất điểm tiêu chí 1, không chèn từ khóa gượng ép. |
| 5 | Cho phép web search | AI tìm quy định Bộ Y tế, nghiên cứu Stanford/UCSF, tài liệu BV Nhi Đồng | Phát hiện: (a) bệnh nhân chờ ra viện chủ yếu do **thanh toán/giám định**, không phải do soạn tóm tắt; (b) bác sĩ *cảm thấy* AI tiết kiệm >10 phút nhưng log chỉ đo được ~3 phút. → Đổi Actor thành bác sĩ, metric đo bằng log, quyết định nghiêng về NOT YET. |
| 6 | "Tiếp tục end to end" | AI viết 01, 02, prototype, vẽ sơ đồ bằng matplotlib | Xem mục 2 về các lỗi phát hiện trong quá trình. |

---

## 2. AI sai ở đâu và đã sửa thế nào

| # | AI sai / hallucination | Phát hiện bằng cách nào | Sửa |
|---|---|---|---|
| A | **Bịa con số không có nguồn:** trong kế hoạch ban đầu AI viết *"khoảng 70% nội dung là dữ liệu có cấu trúc"* — không có nguồn nào cho con số này. | Khi đặt quy ước "mỗi số liệu phải ghi [có nguồn] hay [giả định]", con số này không xếp được vào cột nguồn. | Loại khỏi bài nộp. Trong báo cáo chỉ nói định tính "phần lớn là chép lại dữ liệu có sẵn". |
| B | **Lấy số từ file ví dụ như thể là sự thật:** "20–30 phút/bệnh nhân" ban đầu đến từ `02-deliverable-example.md`, không phải nghiên cứu. | Đối chiếu với web search. | Thay bằng 15–30 phút có nguồn (Stanford), và ghi rõ các thời gian từng bước là `[GĐ]`. |
| C | **Đánh giá rủi ro autograder chưa đủ:** lần đầu AI nói phương án Vinmec "có thể mất 0.5 điểm". | Khi tôi hỏi kỹ, AI đọc lại code: chế độ `--check-code-1` là pass/fail, **không có điểm một phần**. | AI tự đính chính trước khi tôi quyết định. |
| D | **Nhảy vào giải pháp quá sớm** (xem #2 ở trên). | Tôi chủ động hỏi về bước nghiệp vụ. | Bước 0 đã đổi metric từ "bệnh nhân về sớm" (sai) sang "thời gian bác sĩ đo bằng log". |
| E | **Đề xuất làm thêm file Xanh SM** để "chắc điểm" (phương án C). | Tôi thấy nó đi ngược nguyên tắc "không nhét thứ không giải quyết vấn đề". | Bỏ, làm Vinmec trọn vẹn. |
| F | Sơ đồ vẽ lần đầu: ký tự ⏱ không hiển thị, nhãn HANDOFF đè viền ô, mũi tên cắt chú thích. | AI mở ảnh PNG ra xem lại. | Sửa layout, render lại. |

**Ranh giới tôi đặt cho AI trong phiên:**
- Không làm bước nào khi chưa được cho phép; dừng báo cáo sau mỗi bước.
- **Nghiêm cấm đọc file `.env`** — AI chỉ tạo file mẫu, script tự nạp key.
- Không push lên GitHub khi chưa được cho phép.
- Mọi số liệu phải ghi rõ có nguồn hay là giả định.

---

## 3. Kết quả prototype

| Sự kiện | Chuyện gì xảy ra | Xử lý |
|---|---|---|
| Chạy lần 1 | `404 — gemini-2.5-flash no longer available to new users` với key mới. | AI liệt kê các model key được dùng, đưa 3 phương án; **tôi chọn** `gemini-3.8-flash` (Google khuyến nghị), có biến `GEMINI_MODEL` để đổi lại. |
| Chạy lần 2 | Test 1, 3, 4 giữ ranh giới (13/13 check). Test 2 lỗi `503 — model quá tải`. | — |
| **Bug của AI** | Dòng tổng kết in *"13/13 boundary checks OK"* trong khi 1 test không chạy được — **báo cáo trông như đạt hết dù thiếu 1 test**. | AI tự phát hiện khi đọc output: sửa summary để đếm cả test lỗi; thêm retry khi 503/429. |
| Chạy lần 3 | Test 2 giữ ranh giới (không đổi liều, không thêm Clopidogrel); 1 test khác lỗi 503; mất >10 phút. | Ghi nhận: độ ổn định API là rủi ro vận hành thật → fallback sẽ xảy ra thường xuyên. |

**Kết luận:** prompt chưa bị phá ở test nào (4/4 test giữ ranh giới qua các lần chạy), nhưng **6/8 lượt gọi thành công**. Model vẫn chép lại liều thuốc/xét nghiệm vào phần lời văn dù được dặn không — số liệu đúng trong các lần chạy, nhưng validator chưa kiểm tra con số → hướng cải tiến tiếp theo.

---

## 4. Phản ánh cá nhân

> ✍️ *Phần này tôi tự viết.*

**AI giúp tôi nhiều nhất ở đâu?**

> _..._

**Lúc nào tôi phải dừng AI lại / không tin AI?**

> _..._

**Nếu làm lại, tôi sẽ dùng AI khác đi thế nào?**

> _..._
