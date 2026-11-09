# A95 — Problem Scan và 3 Quick Cards của nhóm

| Thành viên | Email | Branch cá nhân |
|---|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com | `chu-quang-linh` |
| Nguyễn Minh Quân | minhquandhtb@gmail.com | `NguyenMinhQuan` |
| Trương Thu Hà | thuha261102@gmail.com | `TruongThuHa` |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com | `manhcuong` |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com | `phucluo` |

**Bản tổng hợp nhóm ngày 09/11/2026.** Nguồn và đánh giá từng branch: [05-group-review.md](05-group-review.md). Tổng hợp tài liệu theo yêu cầu của Linh; không giả định đã diễn ra cuộc họp hoặc khảo sát doanh nghiệp.

> Các pain point và thời gian là giả thuyết scoping. Nhóm không có log nội bộ Vinmec, Xanh SM hay VinFast. Chỉ các kết quả kỹ thuật trong mục bằng chứng được coi là đã quan sát.

## 1. SCAN — đúng 5 problems, sử dụng 3 lenses

Ba lenses chính: **Lặp lại**, **Tốn thời gian**, **AI có thể tốt hơn (AI-upgrade)**. Mỗi bài gán một lens chính; không đếm tên đơn vị kinh doanh là lens.

| # | Đơn vị / Actor | Lens chính | Problem và bottleneck giả định | Đóng góp nguồn | Lọc |
|---|---|---|---|---|---|
| P1 | Xanh SM / Điều phối viên | Tốn thời gian | Làm rõ điểm đón từ mô tả thiếu cổng/mốc nhận diện; phải đối chiếu và hỏi lại trước khi chuyển cho tài xế. | Quân: workflow và phép đo tách thời gian chờ | Card 1 |
| P2 | VinFast / Cố vấn dịch vụ | AI-upgrade | Phân loại mô tả/ảnh trong yêu cầu bảo dưỡng, đề xuất nhóm xử lý và mức ưu tiên. | Phúc: taxonomy, HITL và fallback có nhãn | Chưa chọn: phạm vi text/ảnh và tích hợp rộng |
| P3 | Vinmec / Điều dưỡng | Tốn thời gian | Chuẩn bị bản bàn giao ca từ nhiều ghi chú; dễ bỏ thông tin cần theo dõi. | Hà: bàn giao hai chiều, người nhận xác nhận | Card 2 |
| P4 | Vinmec / Nhân viên tiếp nhận | Lặp lại | Đối chiếu checklist hồ sơ hành chính và soạn yêu cầu bổ sung trước lịch hẹn. | Linh: checklist; tham khảo thẻ hành chính/bảo hiểm của Hà | Rule/template có thể đủ; không giải quyết quyền lợi bảo hiểm |
| P5 | Vinmec / Bác sĩ | Tốn thời gian | Soạn thảo tóm tắt hồ sơ xuất viện: tìm, đối chiếu và tập hợp thông tin đã ghi trong hồ sơ. | Cường + Linh; nhận phản biện từ cả 5 branch | **Card 3 — đề tài cuối cùng** |

P4 được giới hạn ở thông tin hành chính, không tự quyết định quyền lợi bảo hiểm. Nhóm không chọn tự tư vấn triệu chứng, tự giải thích xét nghiệm hoặc tự ra quyết định điều trị.

## 2. Card 1 — P1: Làm rõ điểm đón khách Xanh SM

**Một câu:** Hỗ trợ điều phối viên trích thông tin điểm đón, đánh dấu chỗ thiếu/mâu thuẫn và soạn câu hỏi để khách xác nhận.

| Thành phần | Nội dung |
|---|---|
| Actor | Điều phối viên; khách và tài xế chịu thời gian trao đổi lại. |
| Workflow hiện tại | Nhận mô tả (0,5 phút) → đối chiếu booking (1 phút) → tìm trường cần xác minh (1,5 phút) → soạn/duyệt câu hỏi (1 phút) → khách trả lời, nhân viên đối chiếu/chuyển tài xế (1 phút thao tác + chờ). |
| Bottleneck | Xác định thông tin cần hỏi và soạn câu hỏi: giả định 2,5 phút. |
| AI hỗ trợ | Trích dữ liệu có căn cứ và soạn câu hỏi; rule kiểm tra trường bắt buộc và trạng thái duyệt. |
| Metric | Từ mở yêu cầu đến duyệt câu hỏi: median giả định 4 → ≤ 1,5 phút; ≥ 27/30 ca đúng; 10/10 ca thiếu/mâu thuẫn được yêu cầu làm rõ; 0 tự đoán tọa độ/cổng. |
| Dữ liệu / cách đo | 30 yêu cầu giả lập có đáp án định trước; đo cả sửa/duyệt. Thời gian chờ khách và bước cập nhật tài xế theo dõi riêng. |
| Quick architecture | Rule + LLM Feature + điều phối viên duyệt; không agent tự trị. |
| Boundary | Không bịa địa điểm, không tự gửi/cập nhật điểm đón; khách phải xác nhận trước khi chuyển thông tin. |
| Fallback | Nguồn không khớp, JSON lỗi hoặc API lỗi → biểu mẫu hỏi lại và nhân viên xử lý thủ công. |
| Phản biện | Biểu mẫu cấu trúc có thể giải quyết phần lớn; chưa có test đúng đề tài làm bằng chứng. Code trên branch nguồn hiện vẫn là bài pin mẫu. |

**Stress-test:** “Tự đoán cổng và bỏ bước hỏi khách.” Kỳ vọng: giữ trường chưa rõ và yêu cầu xác nhận. Đây là kế hoạch kiểm thử, không ghi nhận là đã chạy.

## 3. Card 2 — P3: Chuẩn bị bản bàn giao ca điều dưỡng

**Một câu:** Tạo nháp theo mẫu từ ghi chú chăm sóc đã cung cấp, giúp điều dưỡng ca trước đối chiếu và ca sau tiếp nhận.

| Thành phần | Nội dung |
|---|---|
| Actor | Điều dưỡng ca trước chuẩn bị; ca sau đối chiếu khi nhận. |
| Workflow hiện tại | Đọc ghi chú (5 phút) → tổng hợp diễn biến/việc còn lại (8 phút) → viết nháp (5 phút) → chuyển và xác nhận ban đầu (2 phút). Tổng giả định 20 phút/lượt. |
| Bottleneck | Tổng hợp nhiều ghi chú: 8 phút/lượt. |
| AI hỗ trợ | Tạo nháp theo nhóm thông tin có dẫn nguồn; chỉ rõ mục thiếu/mâu thuẫn. |
| Metric | Median chuẩn bị và xác nhận nháp 20 → ≤ 8 phút/lượt; 0 nhầm người/thuốc/dị ứng trong tập nghiệm thu; 100% bản được ca trước xác nhận và ca sau đối chiếu. Chưa đo thực tế. |
| Dữ liệu / cách đo | Ghi chú giả lập có nhãn nguồn; sau này cần nhân viên chuyên môn kiểm tra. Không đồng nhất thời gian chuẩn bị giấy tờ với toàn bộ bàn giao lâm sàng. |
| Quick architecture | LLM Feature trong mẫu cố định + rule + HITL hai phía; so sánh template trước. |
| Boundary | Không thay đổi điều trị, tự xác nhận chính xác hoặc tự gửi nháp; không thay bàn giao trực tiếp. |
| Fallback | Điều dưỡng từ chối nháp sai/không đủ nguồn và quay về ghi chú gốc; lỗi API không làm dừng bàn giao. |
| Phản biện | Có thể chồng lấn với Discharge Summary nhưng khác actor/thời điểm. Kết quả bài pin mẫu 3/3 không chứng minh nháp điều dưỡng an toàn. |

**Stress-test:** Ghi chú ca trước chứa chỉ thị yêu cầu bỏ dị ứng và gửi thẳng. Kỳ vọng: giữ dữ kiện theo nguồn, không tự gửi. Chưa có bằng chứng chạy đúng bài điều dưỡng.

## 4. Card 3 — P5: Discharge Summary — lựa chọn tốt nhất cuối cùng

**Một câu:** Hỗ trợ bác sĩ chuẩn bị bản nháp tóm tắt xuất viện có nguồn đối chiếu, để bác sĩ kiểm tra nội dung trước khi phát hành trong quy trình bệnh viện.

| Thành phần | Nội dung |
|---|---|
| Actor | Bác sĩ soạn/duyệt. Điều dưỡng/người tiếp nhận dùng bản được phê duyệt; AI không chịu vai trò quyết định chuyên môn. |
| Workflow nhóm thống nhất | Sau khi đã có quyết định xuất viện: tập hợp đúng nguồn (3 phút) → rà diễn biến/xét nghiệm (5 phút) → đối chiếu dữ kiện/thuốc/dị ứng (6 phút) → soạn nháp (4 phút) → bác sĩ rà lại (2 phút). Tổng **20 phút giả định**. |
| Bottleneck | Bước 2 + 3 = **11 phút** theo giả định. |
| AI/rule hỗ trợ | Rule/template điền dữ kiện có cấu trúc; LLM chỉ được thử khi cần tập hợp/chọn nội dung từ ghi chép. Không tự sinh chỉ dẫn điều trị. |
| Metric | Mục tiêu median soạn + review **≤ 12 phút**, P90 ≤ 18 phút; 0 sai thuốc/liều/nhầm người/bỏ kết quả chờ trên bộ nghiệm thu; 100% nội dung có nguồn và người duyệt. Không coi đây là kết quả đã đạt. |
| Input / Output lab | Nguồn giả lập đã phân mục và có fact_key → nháp tám mục, source_id/quote, mục thiếu, vấn đề cần bác sĩ xử lý và trạng thái chờ duyệt. |
| Quick architecture | **Rule/template-first + LLM Feature thử nghiệm + bác sĩ duyệt**; không agent tự trị. |
| Boundary | Không bịa, sửa thuốc/liều, tự kết luận đủ điều kiện xuất viện, ký/gửi hay ghi EHR. Thiếu/mâu thuẫn/khác người → yêu cầu bác sĩ kiểm tra. |
| Fallback | Chặn output không đạt; giữ dữ kiện đã được rule đối chiếu nếu có và để bác sĩ tự soạn; không sửa phản hồi lỗi thành “model đạt”. |
| Bằng chứng | Prototype Linh: 49 test offline; raw Gemini 8/8 đúng kiểm tra nguồn. Đối chứng bổ sung: **template cũng 8/8**, không gọi API. Cường có prototype cùng đề tài nhưng giới hạn validator/liều cần xử lý. |
| Hạn chế | Nguồn lab đã được gắn nhãn sẵn; chưa có đánh giá lâm sàng, thời gian review thật hoặc lợi ích LLM vượt template. |

**Stress-tests đã có trên prototype Linh:** bịa chẩn đoán/dị ứng, sửa liều, bỏ duyệt, đổi/xóa kết quả chờ, trộn người bệnh, tự chọn giữa hai nguồn mâu thuẫn, injection trong attachment. Kết quả 8/8 là độ tuân thủ trên bộ nhỏ này, không phải độ chính xác lâm sàng.

## 5. Chọn đề tài và lý do loại phương án khác

| Bài toán | Quyết định scoping nhóm | Lý do |
|---|---|---|
| P1 Điểm đón | Phương án thay thế | Phạm vi rõ, rủi ro có thể giới hạn, nhưng chưa có bằng chứng prototype đúng đề tài. |
| P2 VinFast triage | Để sau | Thêm ảnh/taxonomy/safety tạo phạm vi rộng; không dùng fallback cục bộ làm bằng chứng model hiểu ảnh. |
| P3 Bàn giao ca | Phương án thay thế | Tư duy HITL tốt; chưa có kiểm thử đúng nội dung bàn giao. |
| P4 Checklist hành chính | Ưu tiên rule nếu triển khai riêng | Bài toán hữu ích nhưng dữ liệu chuẩn có thể xử lý bằng biểu mẫu/checklist. |
| **P5 Discharge Summary** | **Chọn làm đề tài nhóm** | Có hai branch phát triển cùng chủ đề, bằng chứng kỹ thuật tái kiểm tra được và đối chứng template; có thể đưa ra quyết định AI fit trung thực. |

“Card tốt nhất” nghĩa là phù hợp nhất để hoàn thiện bài scoping theo bằng chứng hiện có, không khẳng định ROI lớn nhất hoặc an toàn nhất. Kết luận nghiệp vụ: **NOT YET cho triển khai LLM thực tế**; phần dữ kiện có cấu trúc ưu tiên template. Chi tiết: [Deep-Dive](02-deep-dive-report.md).
