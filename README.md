# Nhóm A95 - Lab 02: Discharge Summary

| Thành viên | Email |
|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com |
| Nguyễn Minh Quân | minhquandhtb@gmail.com |
| Trương Thu Hà | thuha261102@gmail.com |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com |

**Bài cá nhân:** Chu Quang Linh — branch `chu-quang-linh`.

Bài toán hiện tại: **Vinmec - Soạn thảo tóm tắt hồ sơ xuất viện**. Prototype tạo bản nháp theo mục từ hồ sơ giả lập, giữ ID/trích dẫn nguồn và bắt buộc bác sĩ duyệt. Chưa kết nối bệnh viện hoặc EHR; không ký, gửi, kê đơn hay quyết định xuất viện.

## Deliverables

- [Problem Scan và ba Quick Cards](01-problem-scan.md).
- [Deep-Dive, workflow tương lai và đánh giá](02-deep-dive-report.md).
- [AI Log và kết quả thực tế](03-ai-log.md).
- [Sơ đồ current-state](04-workflow-diagram.png).
- [Prototype Python](starter-code/prompt_prototype.py).
- [Raw Gemini report](results/gemini-discharge.json).
- [Bản nháp minh họa có thể đọc](output/discharge-summary-demo.md).

Mọi thời gian/hiệu suất nghiệp vụ trong báo cáo là giả định; tên bệnh và thuốc DEMO trong fixture không dùng cho người bệnh thật.

## Thiết lập và chạy trên Windows

Yêu cầu Python 3.12 hoặc 3.13 và Git.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Nếu chưa có .env: copy .env.example .env, rồi điền key vào file cục bộ.
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --report results/gemini-discharge.json
.\.venv\Scripts\python.exe tools/export_discharge_demo.py
.\.venv\Scripts\python.exe tools/render_workflow.py
.\.venv\Scripts\python.exe autograder/autograder.py --section-a
```

Trên macOS/Linux dùng `.venv/bin/python`; script vẽ sơ đồ hiện dùng font Segoe UI trên Windows, cần đổi font nếu tái tạo ở hệ điều hành khác.

Key `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY` trong .env tại thư mục gốc được ưu tiên; nếu thiếu mới dùng biến môi trường. .env đã được Git bỏ qua, không ghi key vào code/log hoặc commit.

Model giữ theo lựa chọn của Linh: **gemini-3.8-flash**, thinking LOW, temperature 0. Tám request độc lập chạy song song, timeout 20 giây mỗi request, không tự retry. Chạy live tiêu tốn quota API.

## Ranh giới và kiểm tra

Output là `[DRAFT_ONLY] ` + JSON gồm action, patient_id, sections, missing_fields, issues và requires_clinician_approval=true.

Tám mục gồm nhập/xuất viện, chẩn đoán, diễn biến, thuốc, dị ứng, tái khám, xét nghiệm chờ và tình trạng xuất viện theo nguồn. Mỗi mục chứa source_id và quote nguyên văn. Validator chặn nguồn không đúng người, đổi text/liều, bỏ nguồn, sai mục và bỏ bác sĩ duyệt.

Thiếu dữ liệu hoặc mâu thuẫn → `request_clinician_review`. Không có vấn đề theo các rule thử nghiệm → `draft_discharge_summary`; vẫn là nháp chưa được bác sĩ phê duyệt. Script chính chỉ chạy fixture tổng hợp, không cung cấp chế độ nhập bệnh án thật.

**Kết quả đã chạy:** 49 test hồi quy đạt; Gemini thật 8/8 cases đạt. Những kiểm tra này không xác nhận độ chính xác lâm sàng của nguồn hoặc tính đầy đủ của hồ sơ thực tế.

Autograder gốc trong `autograder/autograder.py` được giữ nguyên. Section A kiểm tra đủ bốn deliverable; Section B cố định keyword/rule theo use case mẫu ban đầu nên không phù hợp để chấm code Discharge Summary. Không dùng điểm 10/10 của bài trước cho bài hiện tại.

## Quy trình cá nhân và nhóm theo hướng dẫn

1. Mỗi thành viên tạo branch riêng, SCAN ít nhất năm vấn đề và hoàn thiện ba cards.
2. Nhóm thống nhất bài toán; mỗi thành viên vẫn tự hoàn thiện code, tài liệu và AI Log trên branch của mình.
3. Push cả code và tài liệu lên branch cá nhân; **không merge .py cá nhân vào main**.
4. Trưởng nhóm tổ chức review, chọn lọc/tổng hợp tài liệu .md và sơ đồ vào main để nộp bài nhóm.
5. Chỉ trưởng nhóm nộp form. Ghi đầy đủ tên nhóm, họ tên và email thành viên trong deliverable.

Các file [worksheet gốc](01-worksheet.md), [worked example gốc](02-deliverable-example.md) và [inspiration kit](03-inspiration-kit.md) được giữ làm tài liệu lớp; chúng không phải bản lời giải hiện tại.
