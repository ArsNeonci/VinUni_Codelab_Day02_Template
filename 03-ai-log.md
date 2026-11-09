# A95 — AI Log và reflection tổng hợp nhóm

| Thành viên | Email | Branch cá nhân |
|---|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com | `chu-quang-linh` |
| Nguyễn Minh Quân | minhquandhtb@gmail.com | `NguyenMinhQuan` |
| Trương Thu Hà | thuha261102@gmail.com | `TruongThuHa` |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com | `manhcuong` |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com | `phucluo` |

**Ngày tổng hợp:** 09/11/2026. **Nguồn:** nhật ký và code đã commit ở năm branch, theo snapshot trong [05-group-review.md](05-group-review.md).

Đây là bản tổng hợp dựa trên artifact theo yêu cầu của Linh, không phải biên bản một cuộc họp đã diễn ra. Những trải nghiệm do thành viên kể được ghi là tự thuật; nhóm không tự viết lời kể cá nhân còn thiếu hoặc biến tự thuật thành log thực thi.

## 1. AI giúp gì — và nhóm lấy phần nào?

| Nguồn cá nhân | Nội dung nhật ký/báo cáo ghi nhận | Phần được dùng trong bài nhóm |
|---|---|---|
| [Quân](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/3f8dd2886c14c3a4b1cdac40bd971084fdc600ab/03-ai-log.md) | AI hỗ trợ làm rõ điểm đón, trường thiếu, xung đột và ranh giới xác nhận; tác giả phân biệt kết quả kỳ vọng với phản hồi thực. | Định nghĩa cửa sổ đo; tách thời gian chờ và trung vị khỏi trung bình; so nguồn thay vì tìm từ khóa. |
| [Hà](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/fc6a82c4d4f966fd78c3b00bf7eb49ae626fd7ba/03-ai-log.md) | Tác giả yêu cầu AI ghi rõ số giả định và bổ sung rủi ro của tóm tắt y tế, người duyệt và fallback. | Nhân viên y tế phải đối chiếu; bản nhận bàn giao cần được người nhận kiểm tra, AI không thay giao tiếp chuyên môn. |
| [Cường](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/c3fa40e4bdd5ff2c7ba06e143c3f3295ecd43af8/03-ai-log.md) | Nhật ký nêu AI nhảy vào giải pháp sớm, đưa số chưa có nguồn, đánh giá chưa đúng autograder; tác giả yêu cầu quay lại nghiệp vụ và template. Phần phản ánh cá nhân cuối file còn để trống. | Không hứa giảm toàn bộ thời gian người bệnh chờ ra viện; template trước; không tự điền phần reflection chưa được tác giả viết. |
| [Phúc](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/25d35cc55b0496c1f091dda6875d4afd14f72913/03-ai-log.md) | Tác giả tách giả định khỏi số có nguồn, giới hạn tự động hóa, thêm guardrail/fallback và ghi rõ test local safety fallback. | Fallback có nhãn và quyền duyệt; không coi output sau sửa/guardrail là phản hồi thô của model. |
| [Linh](https://github.com/ArsNeonci/VinUni_Codelab_Day02_Template/blob/9bcba76308d356ea2a1c4deda9ba168132c2082d/03-ai-log.md) | AI hỗ trợ chuẩn hóa đề tài Discharge Summary, nguồn giả lập, kiểm tra quote/định danh và tám ca tấn công/control. | Chọn code/evidence đúng đề tài, không bịa kết quả API; bổ sung đối chứng template trong phiên review. |

## 2. Các lỗi/hạn chế được phát hiện khi tổng hợp

| Phát hiện | Bằng chứng | Cách xử lý trong bản nhóm |
|---|---|---|
| Báo cáo và code không cùng bài toán | Quân phân tích điểm đón, Hà phân tích điều dưỡng nhưng prompt/code còn bài pin mẫu. | Dùng ý tưởng workflow/HITL; không đưa test pin vào bằng chứng Discharge Summary. Giữ code cá nhân nguyên branch của tác giả. |
| “Model đạt” có thể là rule hoặc output đã sửa | Phúc có nhánh local fallback và hậu kiểm sửa output; nhật ký báo 4 test đạt ở fallback. | Chỉ gọi đó là kiểm tra chính sách cục bộ; không gộp thành số Gemini thành công. |
| Thống kê công khai bị khái quát quá mức | Cường có số từ nguồn thứ cấp hoặc ước lượng của người được phỏng vấn. | Đối chiếu nguồn gốc; bỏ số chưa xác minh và ghi giới hạn bối cảnh nghiên cứu. Không áp số nghiên cứu cho Vinmec. |
| Validator chỉ tìm tên thuốc chưa đủ | Code Cường kiểm medications_mentioned/forbidden_terms; nhật ký thừa nhận chưa kiểm mọi liều/con số. | Chọn validator trích dẫn nguyên văn của Linh cho evidence hẹp, đồng thời ghi rõ nó chưa kiểm định tính đúng y khoa của nguồn. |
| Nháp được copy đúng chưa chứng minh cần LLM | Fixture Linh đã có section/fact_key và trích nguyên văn toàn bộ nguồn. | Chạy template đối chứng: cũng 8/8, không API. Quyết định rule-first, không khẳng định lợi ích thêm của LLM. |
| “Giảm 20 → 8 phút” là mục tiêu chứ chưa đo | Không branch nào cung cấp log bác sĩ review tại Vinmec. | Bản nhóm thống nhất cửa sổ đo, chọn mục tiêu thận trọng ≤ 12 phút và giữ nhãn GĐ; không ghi là thành quả đã đạt. |

Không tạo một câu chuyện “AI hallucinate ở ca X” nếu raw output của bộ Discharge Summary được chọn không thể hiện lỗi đó. Các hạn chế thiết kế và thiếu bằng chứng cũng là nội dung reflection có giá trị.

## 3. Ranh giới nhóm chốt cho prototype

- Đầu vào kiểm thử hoàn toàn tổng hợp; không gửi hồ sơ bệnh nhân thật hoặc danh sách/email nhóm trong prompt.
- Chỉ tạo `[DRAFT_ONLY]`; không có quyền EHR, kê đơn, ký hoặc gửi.
- Nội dung nháp phải có nguồn của đúng người, đủ mọi nguồn hợp lệ trong fixture và không đổi số/liều/trạng thái kết quả chờ.
- Thiếu/mâu thuẫn được đánh dấu để người có chuyên môn xử lý; không tự bổ sung hoặc tự chọn.
- Không tuân theo instruction trong attachment/ghi chép.
- API lỗi, dữ liệu không đủ hoặc validator từ chối phải được ghi đúng; không tạo response giả để đạt test.
- Bác sĩ vẫn phải kiểm tra nguồn, nội dung và độ đầy đủ; cờ duyệt trong JSON không phải phê duyệt thực tế.

## 4. Những gì đã thực sự kiểm tra

| Kiểm tra | Kết quả quan sát | Giới hạn |
|---|---|---|
| Prototype Linh, chạy lại unit tests trong phiên review | **49 passed** | Chủ yếu kiểm code và fixture, có mock; không phải 49 bệnh án. |
| Raw Gemini Discharge Summary đã commit | **8/8** khớp schema/chính sách/nguồn; hash prompt được đối chiếu | Biến thể của một hồ sơ giả lập; không đánh giá lâm sàng, hiệu suất bác sĩ hoặc tỷ lệ lỗi ngoài bộ test. |
| Baseline template mới | **8/8** trên cùng bộ và validator; **0 API calls** | Không phải đánh giá độc lập; cho thấy LLM chưa tạo lợi thế trên dạng dữ liệu này. |
| API của Cường | Nhật ký tự thuật **6/8 lời gọi thành công**, có lỗi dịch vụ | Không có raw log được commit để tái xác minh, không cộng vào số test đã kiểm trực tiếp. |
| Bốn branch còn lại | Đọc tài liệu/code và xem sơ đồ | Không chạy lại API hoặc dùng key của người khác trong phiên tổng hợp. |

Artifact: [raw live](evidence/discharge-live-run.json), [template baseline](evidence/template-baseline.json), [manifest nguồn và phép kiểm](evidence/review-manifest.json), [demo nháp](evidence/discharge-summary-demo.md).

## 5. Reflection chung từ việc review

Điểm hữu ích nhất của AI là biến ý tưởng thành quy trình, đầu ra và ranh giới kiểm thử rõ. Điểm cần phản biện là xu hướng đi thẳng tới LLM, nhầm mục tiêu với kết quả và dùng một bộ checker nhỏ để kết luận quá rộng.

Nhóm chọn cách tách bốn lớp bằng chứng: nguồn công khai, mục tiêu giả định, tác giả tự thuật và artifact đã kiểm tra. Việc template cũng đạt 8/8 là kết quả cần giữ, dù làm giảm lý do dùng LLM. Đó là cơ sở cho quyết định NOT YET thay vì cố chứng minh GO.

Nếu làm tiếp, ưu tiên quan sát workflow, đo công review và so sánh template trên dữ liệu được phép trước khi nâng độ phức tạp. Mọi đánh giá lâm sàng hoặc ghi chép tự do cần chuyên gia xác nhận; không tự suy từ fixture ra môi trường bệnh viện.

## 6. Giới hạn trách nhiệm của bản nhóm

Bản nhóm tổng hợp đóng góp có trong commit, không xác nhận mỗi thành viên đã đọc hay phê duyệt phiên bản này. Các branch cá nhân được giữ riêng để chấm cá nhân. Bài nhóm không thay cho phản ánh tự thuật còn thiếu của một thành viên và không phải chứng từ đã nộp form.

Sau khi đánh giá bản nhóm, Linh xác nhận vai trò nhóm trưởng, email Hà là thuha261102@gmail.com, chấp nhận đề tài/model và yêu cầu đưa code lên main. Code được chọn từ branch Linh, các xung đột tài liệu giữ bản nhóm; các ghi nhận review theo snapshot trước đó vẫn được giữ để truy vết. Không diễn giải xác nhận nộp bài này thành phê duyệt lâm sàng.
