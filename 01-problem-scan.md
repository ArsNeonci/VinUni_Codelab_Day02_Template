# Nhóm A95 - Problem Scan: Y tế và giáo dục

| Thành viên | Email |
|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com |
| Nguyễn Minh Quân | minhquandhtb@gmail.com |
| Trương Thu Hà | thuha261102@gmail.com |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com |

**Bản cá nhân:** Chu Quang Linh — branch `chu-quang-linh`.

> Đây là scoping giả lập; chưa phỏng vấn Vinmec/VinUni hay truy cập bệnh án thật. Pain point và số liệu dưới đây là giả thuyết/mục tiêu cần kiểm chứng, không phải thống kê doanh nghiệp.

## Phase 1 - SCAN bằng 4 lenses

| # | Đơn vị | Lens | Bài toán cụ thể | Dữ liệu cần xác minh |
|---|---|---|---|---|
| 1 | Vinmec | Tốn thời gian | Bác sĩ phải đọc nhiều ghi chép để soạn tóm tắt hồ sơ xuất viện, dễ bỏ sót thuốc, dị ứng hoặc xét nghiệm chờ. | Bệnh án tổng hợp cho lab; sau này cần hồ sơ được cấp phép, mẫu tóm tắt và bác sĩ gán nhãn. |
| 2 | Vinmec | Lặp lại | Nhân viên đối chiếu hồ sơ hành chính với checklist trước lịch hẹn, phải hỏi bổ sung nhiều lần. | Checklist được duyệt, tin nhắn tổng hợp/ẩn danh, nhãn đủ/thiếu. |
| 3 | VinUni | AI-upgrade | Trợ giảng tra nhiều tài liệu để trả lời câu hỏi về yêu cầu lab và rubric nhất quán, có dẫn nguồn. | Đề bài, rubric, FAQ hiện hành và câu trả lời chuẩn. |
| 4 | Vinmec | Pain từ người khác | Nhân viên nhận các yêu cầu đổi lịch khám viết tự do, phải hỏi lại thông tin hành chính còn thiếu. | Yêu cầu ẩn danh, trường thông tin bắt buộc, danh mục lịch được phép. |
| 5 | VinUni | Lặp lại | Trợ giảng viết lại phản hồi các lỗi code phổ biến sau khi autograder chạy. | Code tổng hợp, output test, rubric và phản hồi được giảng viên duyệt. |
| 6 | VinUni | Tốn thời gian | Giáo vụ đọc nội dung tự do để phân luồng yêu cầu hành chính của sinh viên đến đúng đơn vị. | Ticket tổng hợp, danh mục đơn vị và nhãn đã xác minh. |

## Phase 2 - Ba Quick Problem Cards

### Card 1 - Vinmec: Soạn thảo tóm tắt hồ sơ xuất viện (được chọn)

- **Actor:** Bác sĩ soạn/duyệt; điều dưỡng và người tiếp nhận chăm sóc sử dụng bản được ký.
- **Workflow hiện tại giả định:** Tập hợp hồ sơ (4 phút) → rà diễn biến/xét nghiệm (5 phút) → tổng hợp chẩn đoán/thuốc/dị ứng (6 phút) → viết và đối chiếu (4 phút) → bác sĩ ký/chuyển giao (1 phút).
- **Bottleneck:** Rà và tổng hợp thông tin phân tán chiếm 11/20 phút/lượt theo giả định.
- **AI hỗ trợ:** Tập hợp nội dung thành bản nháp theo mục, mỗi mục gắn ID nguồn; phần thiếu/mâu thuẫn được đánh dấu để bác sĩ giải quyết.
- **Metric mục tiêu:** Median tổng thời gian soạn + duyệt ≤ 8 phút so với baseline giả định 20 phút; P90 ≤ 12 phút; 100% thông tin lâm sàng trong nháp truy được nguồn; 0 thay đổi liều, nhầm người bệnh hoặc bỏ kết quả chờ trên bộ nghiệm thu; 100% cần bác sĩ duyệt.
- **Quick architecture:** Rule + LLM Feature + bác sĩ duyệt; không chọn agent tự trị.
- **Operational boundary:** Không bịa chẩn đoán/kết quả, không sửa thuốc/liều hay tự quyết định xuất viện; không ký/gửi/ghi EHR. Dữ liệu thiếu hoặc mâu thuẫn phải yêu cầu bác sĩ kiểm tra.
- **Dữ liệu lab:** Hồ sơ giả lập, thuốc và bệnh mang tên DEMO; không đưa hồ sơ bệnh nhân thật lên API.

### Card 2 - Vinmec: Kiểm tra hồ sơ hành chính trước lịch hẹn

- **Actor:** Nhân viên tiếp nhận và người đặt lịch.
- **Workflow giả định:** Nhận hồ sơ → đối chiếu checklist → xác định mục thiếu → soạn yêu cầu bổ sung → nhân viên duyệt/gửi.
- **Bottleneck:** Đọc mô tả tự do và trao đổi bổ sung; chưa đo baseline.
- **AI hỗ trợ:** Trích thông tin đã cung cấp và soạn nháp; rule kiểm tra checklist.
- **Metric mục tiêu:** Giảm ≥ 50% median thời gian chuẩn bị yêu cầu bổ sung; F1 phát hiện mục thiếu ≥ 0,95 trên 200 hồ sơ tổng hợp có nhãn; 100% tin gửi cần duyệt.
- **Quick architecture:** Rule + LLM Feature + HITL; biểu mẫu có cấu trúc có thể chỉ cần rule.
- **Boundary/fallback:** Không tư vấn y khoa hoặc tự xác nhận đủ điều kiện khám; không tự tạo giấy tờ ngoài checklist. Thiếu nguồn/mâu thuẫn → nhân viên kiểm tra.

### Card 3 - VinUni: Nháp trả lời FAQ môn học có dẫn nguồn

- **Actor:** Trợ giảng/giảng viên; sinh viên nhận thông tin.
- **Workflow giả định:** Nhận câu hỏi → tra tài liệu hiện hành → đối chiếu → soạn trả lời có nguồn → trợ giảng duyệt/gửi.
- **Bottleneck:** Tìm và đối chiếu đề bài, hướng dẫn, rubric; chưa đo baseline.
- **AI hỗ trợ:** Tìm đoạn liên quan và soạn trả lời có tên file/mục.
- **Metric mục tiêu:** Giảm ≥ 50% median thời gian soạn/duyệt; ≥ 95% câu trả lời đúng và có nguồn hỗ trợ trên 100 câu hỏi chuẩn; 100% câu hỏi không có nguồn/mâu thuẫn chuyển người phụ trách.
- **Quick architecture:** Tìm kiếm/rule theo phiên bản + LLM Feature + HITL; so sánh với FAQ tĩnh.
- **Boundary/fallback:** Không bịa deadline/rubric, không tự chấm/sửa điểm hoặc công bố đáp án chưa được phép. Nguồn mâu thuẫn → dẫn các đoạn và hỏi giảng viên.

## Lựa chọn và phản biện

Chọn **Card 1 - Discharge Summary** theo yêu cầu của Linh. Phạm vi kỹ thuật hẹp: nháp trích xuất có kiểm tra nguồn, không thay bác sĩ ra quyết định y khoa. Bài này kiểm thử được các lỗi cụ thể: sửa liều, bịa nội dung, trộn người bệnh và bỏ xét nghiệm chờ.

Rule/template có thể tự tập hợp nguồn đã gắn nhãn; LLM chỉ đáng giữ khi thực sự tiết kiệm công đọc/chọn nội dung từ ghi chép tự do mà vẫn giữ độ chính xác. Prototype hiện có nguồn đã phân mục nên chưa chứng minh LLM tốt hơn rule. Card 2 và 3 là phương án thay thế nếu dữ liệu/khả năng giám sát lâm sàng chưa đáp ứng.

Chi tiết thiết kế và đánh giá: [Deep-Dive](02-deep-dive-report.md).
