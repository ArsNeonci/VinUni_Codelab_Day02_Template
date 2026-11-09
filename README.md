# A95 — Bài nộp nhóm Lab 02: AI Product Scoping

| Thành viên | Email | Branch cá nhân |
|---|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com | `chu-quang-linh` |
| Nguyễn Minh Quân | minhquandhtb@gmail.com | `NguyenMinhQuan` |
| Trương Thu Hà | thuha261102@gmail.com | `TruongThuHa` |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com | `manhcuong` |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com | `phucluo` |

**Đề tài nhóm:** Vinmec — Soạn thảo tóm tắt hồ sơ xuất viện (Discharge Summary).

Đây là bản tổng hợp từ năm branch cá nhân. Mục tiêu là giảm công bác sĩ tìm, đối chiếu và soạn tài liệu; không thay bác sĩ quyết định điều trị hoặc xuất viện. Bài dùng dữ liệu giả lập, không có dữ liệu bệnh nhân thật hay tích hợp bệnh viện.

## Bộ bài nhóm trên main

| File | Nội dung |
|---|---|
| [01-problem-scan.md](01-problem-scan.md) | Đúng 5 problems, 3 lenses, 3 Quick Cards; Discharge Summary là Card 3 cuối cùng. |
| [02-deep-dive-report.md](02-deep-dive-report.md) | G1 workflow, G2 sáu trường/metrics, G3 AI fit/HITL/fallback, G4 chi phí/readiness/quyết định. |
| [03-ai-log.md](03-ai-log.md) | Nhật ký và reflection tổng hợp có nguồn cá nhân, phân biệt lời kể với artifact. |
| [04-workflow-diagram.png](04-workflow-diagram.png) | Current/future state, bottleneck, handoff, thời gian giả định và fallback. |
| [05-group-review.md](05-group-review.md) | Đánh giá từng branch theo rubric, lý do chọn lọc và commit nguồn cố định. |
| [evidence/review-manifest.json](evidence/review-manifest.json) | Snapshot nguồn và phạm vi kiểm tra. |

## Kết quả và kết luận

- **49 unit tests** prototype Linh được chạy lại thành công.
- **8/8** phản hồi Gemini thật đã lưu khớp kiểm tra nguồn; hash prompt được đối chiếu.
- **Template cũng 8/8** trên cùng fixture và validator, không phát sinh API calls trong so sánh.
- Vì input đã phân mục, kết quả chưa chứng minh LLM tốt hơn template. **NOT YET cho triển khai LLM thực tế; rule/template là mặc định cho dữ kiện có cấu trúc.**
- Mốc **20 → 12 phút** là baseline/mục tiêu giả định theo cùng cửa sổ thao tác, không phải hiệu quả đã đo. Không tuyên bố giảm toàn bộ thời gian người bệnh chờ xuất viện.

Evidence: [raw live](evidence/discharge-live-run.json), [template](evidence/template-baseline.json), [demo nháp giả lập](evidence/discharge-summary-demo.md).

## Code chạy trên main

Theo yêu cầu cuối cùng của Chu Quang Linh với vai trò nhóm trưởng, code Discharge Summary được chọn từ branch `chu-quang-linh` đã được tích hợp vào main, cùng tests, công cụ demo và dependencies. Báo cáo và sơ đồ giữ bản tổng hợp nhóm. Đây là thay đổi theo xác nhận trực tiếp của nhóm trưởng sau bản tổng hợp tài liệu ban đầu.

Code hiện tại: [prototype](starter-code/prompt_prototype.py), [tests](tests/test_prompt_prototype.py), [template comparison](tools/compare_template_baseline.py), [xuất demo](tools/export_discharge_demo.py) và [vẽ sơ đồ nhóm](tools/render_workflow.py). Commit nguồn được giữ trong [manifest](evidence/review-manifest.json).

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Nếu chưa có .env: copy .env.example .env rồi điền GEMINI_API_KEY cục bộ.
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools/compare_template_baseline.py
.\.venv\Scripts\python.exe tools/export_discharge_demo.py
.\.venv\Scripts\python.exe tools/render_workflow.py
# Chỉ chạy dòng sau khi muốn gọi lại Gemini thật (8 ca tổng hợp, tiêu tốn quota):
.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --report results/gemini-discharge.json
```

Key được nạp từ `.env` tại gốc repo, không ghi vào log hoặc commit. `results/` là đầu ra có thể tái tạo; `evidence/` giữ snapshot đã dùng để tổng hợp báo cáo. Công cụ vẽ dùng font Segoe UI trên Windows. Chỉ dùng hồ sơ giả lập trong prototype này.

Các branch cá nhân khác được liên kết trong file review; không coi việc có tên trong báo cáo là thay cho bài/commit cá nhân. Không gán điểm cá nhân thay giảng viên.

## Kiểm tra bộ file nhóm

```powershell
python autograder/autograder.py --section-a
```

Section A chỉ kiểm tra sự tồn tại bốn deliverable, không chấm chất lượng nội dung. Section B kiểm tra keyword/rule cố định của bài pin mẫu nên không dùng làm điểm code của nhóm. Không chèn keyword sai đề tài để qua checker.

Các file [worksheet](01-worksheet.md), [worked example](02-deliverable-example.md) và [inspiration kit](03-inspiration-kit.md) giữ nguyên làm tài liệu lớp.

## Quy trình nộp theo hướng dẫn

1. Các branch cá nhân được giữ nguyên để truy vết; nhóm trưởng đã yêu cầu đưa code được chọn lên main cùng tài liệu nhóm.
2. Bản main hiện là bộ tài liệu nhóm để trưởng nhóm dùng nộp. Các giả định, nguồn và giới hạn đã ghi trong báo cáo.
3. Chỉ trưởng nhóm điền form theo tài liệu lớp, với họ tên và link repository: [Form được PDF hướng dẫn](https://forms.gle/nzwFKAooNbb7iot36). Phiên tổng hợp này không gửi form và không xác nhận nhóm đã nộp.
4. Mỗi người tự xác nhận email đăng ký BTC đã liên kết tài khoản GitHub; repo không cho biết trạng thái đăng ký đó.

Nhóm trưởng đã xác nhận email của Hà là `thuha261102@gmail.com` và chấp nhận đề tài Discharge Summary/model Gemini 3.8. Tên/email nhóm dùng danh sách Linh đã cung cấp. Xác nhận này không phải phê duyệt sử dụng prototype trong bệnh viện.
