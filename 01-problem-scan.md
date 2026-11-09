# 01 — Problem Scan
**Tên nhóm:** A95
**Thành viên:**
- Trương Thị Thu Hà — 26ai.hattt@vinuni.edu.vn

## Phase 1 — SCAN (tối thiểu 5 bài toán)
| # | Subsidiary | Lens | Mô tả ngắn bài toán | Con số minh họa |
|---|---|---|---|---|
| 1 | Vinmec | Lặp lại (Repetitive) | Khi lịch khám thay đổi, nhân viên phải cập nhật thông tin và gửi lại thông báo cho bệnh nhân qua nhiều kênh, dễ mất thời gian và sai sót. | 3–5 phút/lịch thay đổi, 10–15 lịch/ngày |
| 2 | Vinmec | Tốn thời gian (Time-consuming) | Nhân viên hành chính mất nhiều thời gian kiểm tra giấy tờ và đối chiếu điều kiện bảo hiểm trước khi hoàn thiện hồ sơ thanh toán. | 5–10 phút/hồ sơ, 10–20 hồ sơ/ngày |
| 3 | Vinmec | Tốn thời gian (Time-consuming) | Điều dưỡng mất nhiều thời gian đọc ghi chú và tổng hợp tình trạng bệnh nhân để bàn giao giữa các ca trực. | 15–25 phút/ca trực, 2–3 ca/ngày |
| 4 | Vinmec | AI có thể tốt hơn (AI-upgrade) | Phản hồi của bệnh nhân được thu thập nhưng việc phân loại, tìm nguyên nhân phàn nàn và nhận diện vấn đề lặp lại còn cần nhiều thao tác thủ công. | 50 phản hồi/tuần, 45–60 phút phân tích thủ công |
| 5 | Vinmec | Pain từ người khác (Stakeholder Pain) | Bệnh nhân khám nhiều chuyên khoa có thể không biết nên đến khu vực nào tiếp theo, phải hỏi nhân viên nhiều lần và di chuyển không cần thiết. | 2–3 lần hỏi đường/lượt khám, mất thêm 10–15 phút |

## Phase 2 — 3 Quick Problem Cards
Chọn 3 bài từ bảng SCAN: #3 (bàn giao ca điều dưỡng), #2 (đối chiếu hồ sơ bảo hiểm), #4 (phân tích phản hồi bệnh nhân).

## Card #3 — Hỗ trợ bàn giao ca điều dưỡng bằng AI

**Công ty thành viên:** Vinmec

**Lens:** Tốn thời gian (Time-consuming)

**1. Ai đang khổ:**
- Điều dưỡng tại các khoa nội trú của Vinmec, đặc biệt khi phải bàn giao nhiều bệnh nhân giữa các ca trực.

**2. Quy trình hiện tại (4 bước, thời gian tính cho mỗi ca trực):**
1. Đọc hồ sơ và ghi chú chăm sóc của các bệnh nhân được phân công trong ca (5 phút).
2. Tổng hợp diễn biến, thuốc đã sử dụng và các công việc cần theo dõi (8 phút).
3. Soạn nội dung bàn giao ca trực (5 phút).
4. Kiểm tra thông tin và trao đổi với điều dưỡng ca tiếp theo (2 phút).

**3. Bước tốn thời gian nhất + số phút:**
- Bước 2: Tổng hợp thông tin bệnh nhân, khoảng **8 phút/ca**.

**4. AI giúp ở bước nào:**
- Bước 1–3: LLM đọc ghi chú đã được cung cấp, trích xuất thông tin quan trọng và tạo bản nháp bàn giao theo cấu trúc chuẩn.
- Điều dưỡng kiểm tra, chỉnh sửa và phê duyệt kết quả trước khi bàn giao.

**5. Mục tiêu:**
- Giảm tổng thời gian chuẩn bị và bàn giao từ **20 phút xuống 8 phút/ca**, tiết kiệm khoảng 60%.

**6. Giải pháp: LLM**
- Sử dụng mô hình ngôn ngữ lớn để tóm tắt và cấu trúc lại thông tin. Không để AI tự đưa ra quyết định điều trị.

---

## Card #2 — Hỗ trợ kiểm tra và đối chiếu hồ sơ bảo hiểm

**Công ty thành viên:** Vinmec

**Lens:** Tốn thời gian (Time-consuming)

**1. Ai đang khổ:**
- Nhân viên hành chính và bộ phận xử lý bảo hiểm tại Vinmec.

**2. Quy trình hiện tại (4 bước):**
1. Tiếp nhận giấy tờ bảo hiểm và thông tin bệnh nhân (1 phút).
2. Kiểm tra thông tin trên từng giấy tờ (3 phút).
3. Đối chiếu thông tin với dữ liệu đăng ký và checklist yêu cầu (4 phút).
4. Ghi nhận lỗi, yêu cầu bổ sung hoặc chuyển hồ sơ xử lý (2 phút).

**3. Bước tốn thời gian nhất + số phút:**
- Bước 3: Đối chiếu thông tin, khoảng **4 phút/hồ sơ**, nhân với 10–20 hồ sơ/ngày.

**4. AI giúp ở bước nào:**
- Bước 2: LLM hỗ trợ trích xuất dữ liệu từ giấy tờ.
- Bước 3: Rule kiểm tra các trường thông tin bắt buộc, đối chiếu và đánh dấu những mục thiếu hoặc không khớp.
- Bước 4: Tạo checklist để nhân viên rà soát và xử lý.

**5. Mục tiêu:**
- Giảm tổng thời gian xử lý từ **10 phút xuống 3 phút/hồ sơ**, tiết kiệm khoảng 70%.

**6. Giải pháp: Rule + LLM**
- Rule: Kiểm tra các điều kiện và quy tắc đối chiếu đã xác định.
- LLM: Hỗ trợ đọc và trích xuất thông tin từ giấy tờ.
- Nhân viên xác minh kết quả; AI không tự quyết định quyền lợi hay mức chi trả bảo hiểm.

---

## Card #4 — Phân loại và phân tích phản hồi bệnh nhân bằng AI

**Công ty thành viên:** Vinmec

**Lens:** AI có thể tốt hơn (AI-upgrade)

**1. Ai đang khổ:**
- Nhân viên chăm sóc khách hàng và bộ phận quản lý chất lượng dịch vụ của Vinmec.

**2. Quy trình hiện tại (4 bước):**
1. Thu thập 50 phản hồi từ các kênh khảo sát và chăm sóc khách hàng (5 phút).
2. Đọc và xác định nội dung chính của từng phản hồi (25 phút).
3. Phân loại phản hồi theo chủ đề, mức độ ưu tiên và vấn đề nổi bật (20 phút).
4. Tổng hợp kết quả thành báo cáo (10 phút).

**3. Bước tốn thời gian nhất + số phút:**
- Bước 2: Đọc và xác định nội dung của 50 phản hồi, khoảng **25 phút/50 phản hồi**.

**4. AI giúp ở bước nào:**
- Bước 2: LLM đọc và tóm tắt nội dung phản hồi.
- Bước 3: Tự động phân loại theo chủ đề như thời gian chờ, thái độ phục vụ, chi phí và cơ sở vật chất.
- Bước 4: Tổng hợp số lượng theo nhóm vấn đề và tạo bản nháp báo cáo, đánh dấu phản hồi cần nhân viên xem xét.

**5. Mục tiêu:**
- Giảm thời gian xử lý từ **60 phút xuống 15 phút/50 phản hồi**, tiết kiệm khoảng 75%.

**6. Giải pháp: LLM**
- Sử dụng LLM để phân loại văn bản, trích xuất vấn đề và tạo báo cáo tổng hợp. Nhân viên kiểm tra những trường hợp phân loại chưa chắc chắn.
