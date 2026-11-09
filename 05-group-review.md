# A95 — Review các branch và truy vết bản tổng hợp

| Thành viên | Email | Branch cá nhân |
|---|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com | `chu-quang-linh` |
| Nguyễn Minh Quân | minhquandhtb@gmail.com | `NguyenMinhQuan` |
| Trương Thu Hà | thuha261102@gmail.com | `TruongThuHa` |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com | `manhcuong` |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com | `phucluo` |

**Review ngày 09/11/2026.** Đây là đánh giá nội bộ phục vụ tổng hợp bài, không phải điểm giảng viên và không phải biên bản đồng thuận của năm người. Không sửa các branch của thành viên khác.

## 1. Snapshot đã đọc

| Thành viên / branch | Commit cố định | Tài liệu chính |
|---|---|---|
| Quân — NguyenMinhQuan | `3f8dd2886c14c3a4b1cdac40bd971084fdc600ab` | [Scan](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/3f8dd2886c14c3a4b1cdac40bd971084fdc600ab/01-problem-scan.md), [Deep-Dive](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/3f8dd2886c14c3a4b1cdac40bd971084fdc600ab/02-deep-dive-report.md), [AI Log](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/3f8dd2886c14c3a4b1cdac40bd971084fdc600ab/03-ai-log.md) |
| Hà — TruongThuHa | `fc6a82c4d4f966fd78c3b00bf7eb49ae626fd7ba` | [Scan](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/fc6a82c4d4f966fd78c3b00bf7eb49ae626fd7ba/01-problem-scan.md), [Deep-Dive](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/fc6a82c4d4f966fd78c3b00bf7eb49ae626fd7ba/02-deep-dive-report.md), [AI Log](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/fc6a82c4d4f966fd78c3b00bf7eb49ae626fd7ba/03-ai-log.md) |
| Linh — chu-quang-linh | `9bcba76308d356ea2a1c4deda9ba168132c2082d` | [Scan](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/9bcba76308d356ea2a1c4deda9ba168132c2082d/01-problem-scan.md), [Deep-Dive](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/9bcba76308d356ea2a1c4deda9ba168132c2082d/02-deep-dive-report.md), [AI Log](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/9bcba76308d356ea2a1c4deda9ba168132c2082d/03-ai-log.md) |
| Cường — manhcuong | `c3fa40e4bdd5ff2c7ba06e143c3f3295ecd43af8` | [Scan](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/c3fa40e4bdd5ff2c7ba06e143c3f3295ecd43af8/01-problem-scan.md), [Deep-Dive](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/c3fa40e4bdd5ff2c7ba06e143c3f3295ecd43af8/02-deep-dive-report.md), [AI Log](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/c3fa40e4bdd5ff2c7ba06e143c3f3295ecd43af8/03-ai-log.md) |
| Phúc — phucluo | `25d35cc55b0496c1f091dda6875d4afd14f72913` | [Scan](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/25d35cc55b0496c1f091dda6875d4afd14f72913/01-problem-scan.md), [Deep-Dive](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/25d35cc55b0496c1f091dda6875d4afd14f72913/02-deep-dive-report.md), [AI Log](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/25d35cc55b0496c1f091dda6875d4afd14f72913/03-ai-log.md) |

Linh có commit bổ sung baseline sau bản cá nhân d25e942; không đổi system prompt hay code prototype. Review gồm ba .md, sơ đồ và đọc tĩnh .py của mỗi branch. Chỉ prototype Linh do phiên làm việc này đã phát triển được import/run test để xác minh evidence; không thực thi tùy tiện code của các branch khác.

Thông tin nhóm ở đầu các file dùng đúng danh sách Linh đã cung cấp. Branch Hà ghi tên “Trương Thị Thu Hà” và email VinUni khác danh sách này; review không tự thay thông tin đăng ký hoặc sửa branch của Hà.

## 2. Rubric dùng để đánh giá

Theo worksheet: **G1 Workflow 20**, **G2 Problem Statement 20**, **G3 AI Fit/Future Flow 10**, **G4 Decision Quality 10**. I1/I2/I3 là điểm cá nhân, không tự cấp điểm hoặc thay bài cá nhân bằng bản nhóm.

## 3. Đánh giá từng bài

| Nguồn | G1 — workflow/handoff | G2 — problem/metric | G3 — fit/boundary | G4 — quyết định/bằng chứng | Hạn chế cần giữ rõ |
|---|---|---|---|---|---|
| **Quân** | Rõ từng bước, vòng hỏi lại và thời gian chờ; ảnh dễ đọc. | Sáu trường rõ; tách 4 phút chuẩn bị câu hỏi khỏi tổng 5 phút thao tác + chờ; dùng mean cho công tiết kiệm. | So Rule/LLM/Agent và xác nhận hai phía tốt. | NOT YET vì chưa tạo/đo bộ 30 ca; không giả định mục tiêu là kết quả. | Code tại commit vẫn prompt/test pin Xanh SM, không phải prototype điểm đón; thiếu metadata nhóm ở đầu báo cáo. |
| **Hà** | Quy trình điều dưỡng và xác nhận người nhận rõ, ảnh bốn bước đúng thời gian. | Sáu trường, tổng và bottleneck có số; một số câu cần giữ nhãn giả định xuyên suốt. | Boundary y tế và fallback cụ thể; không thay bàn giao trực tiếp. | Phân biệt sandbox và thực tế. | Báo cáo điều dưỡng nhưng code/test là pin Xanh SM; “có thể tạo dữ liệu” chưa phải đã có dataset nghiệp vụ. |
| **Linh** | Sơ đồ sạch, có handoff/thời gian. | Đủ năm vấn đề/ba lens/ba card; metric rõ và ghi GĐ. | Schema và validator nguồn khớp code; chặn sai người/quote/thiếu. | Raw API và tests có thể đối chiếu; thừa nhận chưa hơn template. | Nháp còn là trích xuất từ nguồn phân mục, chưa tóm tắt ghi chép tự do; không có review lâm sàng. |
| **Cường** | Current/future trong một ảnh; tách chữ ký/thanh toán khỏi công soạn. | Actor bác sĩ, metric log và tự phản biện mạnh. | Template + LLM hẹp, fallback giữ template; loại agent hợp lý. | NOT YET; ghi cả lỗi dịch vụ và điểm yếu validator. | Một số số nguồn cần diễn giải đúng bối cảnh; validator tên thuốc chưa đảm bảo liều/toàn bộ text; reflection cá nhân cuối file còn trống. |
| **Phúc** | Workflow, input/output và handoff khá đầy đủ; ảnh rất cao nên khó đọc tổng thể. | Metric đa chiều và công thức chi phí rõ. | Rule guardrail, confidence/manual-review và fallback có nhãn. | NOT YET; điều kiện pilot có cấu trúc. | Chưa có proof vision/accuracy theo đề tài; test local fallback không phải live model. Baseline 3–5 và 8–14 phút phải phân biệt cửa sổ đo. |

Không xếp một bài “đạt hết” chỉ vì có nhiều chữ, ảnh đẹp hoặc checker có chữ Passed. Ưu tiên nội dung nhất quán với code, nguồn số liệu và ranh giới đã thử.

## 4. Quyết định chọn lọc

| Nội dung bản nhóm | Nguồn chọn / cách chỉnh |
|---|---|
| Đề tài Discharge Summary | Cường + Linh cùng phân tích; giữ lựa chọn trước đó của Linh. |
| SCAN 5 problems / 3 lenses | Tổng hợp điểm đón (Quân), triage VinFast (Phúc), bàn giao điều dưỡng (Hà), hành chính (Linh/Hà), discharge (Cường/Linh). |
| 3 cards | Điểm đón, bàn giao ca, Discharge Summary đặt cuối và được chọn; hai bài còn lại được lọc có lý do. |
| Cửa sổ đo và metric | Lấy cách tách thao tác/chờ của Quân và công bác sĩ của Cường; thống nhất nhóm 20 phút GĐ → mục tiêu ≤ 12 phút, không trộn các scope cá nhân. |
| Thiết kế | Template-first từ Cường; nguyên tắc xác nhận/bàn giao của Hà; fallback phân biệt loại từ Phúc; validator nguồn của Linh. |
| Bằng chứng | Chọn raw report Linh đúng đề tài; bổ sung template đối chứng và ghi shared-validator limitation. |
| Quyết định | NOT YET cho triển khai LLM vì dữ liệu/giá trị thêm chưa được chứng minh; rule/template mặc định cho cấu trúc hiện tại. |
| Sơ đồ | Vẽ lại chung current/future/fallback với cùng tên bước, tổng thời gian và scope của báo cáo. |
| AI Log | Tổng hợp có attribution, không viết thay phần phản ánh cá nhân còn thiếu, không giả định họp đã diễn ra. |

## 5. Các nội dung không nhập nguyên văn

1. Không lấy test pin của Hà/Quân làm test nghiệp vụ y tế.
2. Không cộng 4/4 boundary qua các lần chạy thành “API 100% thành công” nếu có lỗi dịch vụ.
3. Không dùng fallback/đầu ra đã ép tag làm bằng chứng prompt gốc tuân thủ.
4. Không mang tỷ lệ hallucination của GPT trong nghiên cứu cấp cứu sang Gemini hay Vinmec.
5. Không ghi template “chính xác tuyệt đối/an toàn gần bằng 0”: nguồn hoặc mapping có thể sai; con người vẫn cần kiểm tra.
6. Không đưa thời gian chờ thanh toán vào mục tiêu giảm công soạn.
7. Không tuyên bố đã được bệnh viện/bác sĩ duyệt, có bệnh án thật hay đã nộp form.
8. Không thêm keyword điều xe vào prompt y tế chỉ để qua autograder cũ.

## 6. Bằng chứng mới và giới hạn

- 49 unit tests prototype Linh chạy lại thành công trong phiên này.
- Raw live Gemini: 8/8, hash prompt khớp code nguồn được chọn; **không gọi lại API** trong phiên tổng hợp.
- Template đối chứng: 8/8 trên cùng fixture và validator, 0 API calls; code ở [branch cá nhân](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/9bcba76308d356ea2a1c4deda9ba168132c2082d/tools/compare_template_baseline.py).
- Bộ tám ca là biến thể tổng hợp, không phải holdout lâm sàng; không ghi nhận thời gian bác sĩ hay chi phí token.
- Nguồn công khai có thể đọc lại: AHRQ, Stanford Medicine và preprint Williams được dẫn với giới hạn trong [Deep-Dive](02-deep-dive-report.md).

Raw evidence được lấy nguyên từ Git blob. Hash file trong báo cáo baseline ban đầu dùng byte CRLF của Windows; manifest kèm hash chuẩn hóa LF và ghi cách đối chiếu để không nhầm khác xuống dòng với khác nội dung. System prompt được kiểm tra riêng theo SHA-256.

## 7. Tích hợp Git

Chỉ nhập tài liệu, ảnh và evidence. File .py cá nhân, tests .py, script vẽ .py, key và .env không đưa vào commit nhóm. Các .py sẵn có trên main là template/autograder gốc và phải giữ nguyên so với commit nền.

Bài nhóm chính gồm 01-problem-scan.md, 02-deep-dive-report.md, 03-ai-log.md và 04-workflow-diagram.png. README, file review và evidence hỗ trợ kiểm tra/tái lập. Các branch cá nhân không bị merge vào main.
