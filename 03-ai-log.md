# Nhóm A95 - AI Log: Discharge Summary

| Thành viên | Email |
|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com |
| Nguyễn Minh Quân | minhquandhtb@gmail.com |
| Trương Thu Hà | thuha261102@gmail.com |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com |

**Bản cá nhân:** Chu Quang Linh — Quanglinh1286@gmail.com; branch `chu-quang-linh`.

> Nhật ký ghi lại phiên dùng Codex theo yêu cầu của Linh. Không tự gán trải nghiệm hoặc đóng góp cho thành viên khác. Tất cả hồ sơ, tên bệnh/thuốc và số liệu trong fixture là giả lập.

## Yêu cầu và phạm vi mới

Linh yêu cầu thay bài toán đã triển khai bằng **Soạn thảo tóm tắt hồ sơ xuất viện (Discharge Summary)**. AI chuyển code, test, báo cáo và sơ đồ sang bản nháp cho bác sĩ Vinmec, giữ model gemini-3.8-flash và cách đọc key từ .env đã được yêu cầu trước đó.

AI dùng định hướng nội dung từ [AHRQ Care Transitions](https://psnet.ahrq.gov/perspective/care-transitions) và [RED Toolkit Tool 3](https://www.ahrq.gov/patient-safety/settings/hospital/red/toolkit/redtool3.html): cần chú ý thông tin điều trị đã ghi, thuốc, theo dõi và kết quả chờ. Không sử dụng các nguồn này để tự tạo điều trị cho người bệnh.

## AI hỗ trợ và lựa chọn thiết kế

AI giúp viết SCAN, ba problem cards, Problem Statement 6-field, workflow, mục tiêu đo lường và readiness. Các thời gian 20 phút → 8 phút là giả thuyết cần khảo sát, không phải kết quả đo.

Prototype dùng hồ sơ SYNTH-001 và SYNTH-002, tên bệnh/thuốc mang nhãn mô phỏng/DEMO. Không đưa tên hay email thành viên trong prompt API. Không truy cập bệnh án thật.

Thay vì cho LLM tự diễn giải bệnh án rồi chỉ kiểm tra vài từ khóa, nháp phải có tám mục và từng trích dẫn phải khớp toàn bộ nguồn theo ID. Điều này cho phép test phát hiện cụ thể việc đổi liều, thêm chẩn đoán hoặc đổi trạng thái xét nghiệm. Đổi lại, đây là nháp trích xuất theo mục, chưa chứng minh khả năng rút gọn bệnh án tự do hay lợi ích so với template.

## Những ranh giới đã đưa vào prompt và code

1. Mọi phản hồi bắt đầu [DRAFT_ONLY], luôn requires_clinician_approval=true; không ký, gửi hay ghi EHR.
2. Không bịa, đổi nội dung hoặc thêm khuyến nghị điều trị; các thuốc DEMO chỉ là token kiểm thử.
3. Thiếu mục → để trống và báo missing_data; không suy ra “không có dị ứng” từ việc chưa có nguồn.
4. Nguồn khác người bệnh → loại khỏi nháp và báo mixed_patient_records.
5. Hai nguồn cùng fact_key khác nội dung → giữ cả hai để đối chiếu, báo conflicting_records; không tự chọn đơn thuốc.
6. Xét nghiệm chờ phải giữ nguyên; instruction trong attachment không được coi là system prompt.
7. Output rỗng/API lỗi/không khớp nguồn phải trả lỗi, không tạo câu trả lời giả để đạt test.

## Kết quả đã quan sát

| Kiểm tra | Kết quả | Bằng chứng và giới hạn |
|---|---|---|
| Pytest offline | **49/49 đạt** | Kiểm tra cấu trúc, nguồn, liều, dị ứng, kết quả chờ, nhầm người, mâu thuẫn, .env, SDK và exit code. SDK mock, không phải Gemini thật. |
| Gemini thật | **8/8 đạt**, exit 0 | [Raw report](results/gemini-discharge.json), có model, timestamp và hash system prompt; bảy adversarial cases + một control. |
| Autograder gốc Section A | **5/5**, exit 0 | Đủ bốn file deliverable; không dùng Section B cố định cho bài mẫu khác để kết luận về code mới. |
| Đánh giá lâm sàng | **Chưa có** | Chưa có bác sĩ xác minh tính đầy đủ của schema, nguồn hoặc khả năng áp dụng cho bệnh án thực tế. |

Ở lượt Gemini thật của bài mới, chưa quan sát trường hợp vi phạm các kiểm tra đã định nghĩa; không ghi nhận giả rằng đã xảy ra hallucination nếu không có bằng chứng. Các case ép mô hình bịa chẩn đoán, tăng liều và xóa kết quả chờ đều được kiểm tra bằng đối chiếu nội dung nguyên bản, không chỉ tìm chữ “an toàn”.

Autograder gốc không bị chỉnh sửa để tạo điểm đạt: phần code của nó kiểm tra keyword/rule của một bài mẫu khác. Chỉ Section A dùng để kiểm tra file; kiểm chứng cho Discharge Summary dựa trên pytest và live report mới. Các log/điểm của bài toán trước được bỏ khỏi bộ deliverable hiện tại để tránh nhầm bằng chứng.

## Tái lập

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --report results/gemini-discharge.json
.\.venv\Scripts\python.exe tools/export_discharge_demo.py
.\.venv\Scripts\python.exe tools/render_workflow.py
.\.venv\Scripts\python.exe autograder/autograder.py --section-a
```

## Reflection

AI hữu ích khi biến yêu cầu chung thành ranh giới có thể kiểm tra: đúng người, nguyên vẹn nguồn, giữ thông tin chờ và bác sĩ duyệt. Nhận ra phần đối chiếu ID/quote/missing_fields phù hợp rule hơn là để LLM tự phán đoán. Với nguồn đã phân mục sẵn, template là baseline mạnh và chưa có bằng chứng cần LLM.

8/8 test không chứng minh an toàn y khoa: nguồn có thể sai, gắn sai section hoặc thiếu thông tin chưa có trong fixture. Cần bác sĩ review, dữ liệu được cấp phép, bộ kiểm định độc lập và đo cả thời gian sửa nháp trước khi xét pilot.

Bản cá nhân được cập nhật trên branch của Linh. Các thành viên khác cần ghi reflection thực tế của họ và hoàn thành code trên branch riêng; trưởng nhóm chọn lọc tài liệu vào main theo quy định.
