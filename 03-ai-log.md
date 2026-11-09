# Nhóm A95 - AI Log & Reflection

**Bản nộp cá nhân:** Chu Quang Linh — Quanglinh1286@gmail.com; branch `chu-quang-linh`.

| Thành viên | Email |
|---|---|
| Chu Quang Linh | Quanglinh1286@gmail.com |
| Nguyễn Minh Quân | minhquandhtb@gmail.com |
| Trương Thu Hà | thuha261102@gmail.com |
| Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com |
| Nguyễn Lương Phúc | luongphuc.lpu@gmail.com |

> Nhật ký của phiên thực hiện bằng Codex theo yêu cầu người dùng. Không thay thế phản ánh cá nhân của từng thành viên, không tự gán đóng góp hoặc quan sát thực địa chưa xảy ra.

## Yêu cầu đã nhận và AI hỗ trợ

Người dùng yêu cầu đọc PDF Day 02 và thực hiện vào source code; sau đó cung cấp tên nhóm, danh sách thành viên và yêu cầu dùng Gemini API key trong `.env`. AI đọc 21 trang PDF, đối chiếu README, worksheet, code mẫu và autograder; chọn bài toán Xanh SM đang có sẵn để hoàn thiện prototype và các deliverable nhất quán.

AI hỗ trợ xây dựng SCAN bằng 4 lenses, ba problem cards, workflow hiện tại/tương lai, metric và checklist readiness. Những con số nghiệp vụ được ghi là giả định. AI không thực hiện khảo sát và không biến số trong worked example thành số liệu của nhóm.

## Điểm thiếu chặt chẽ được phát hiện và điều chỉnh

1. **Output format chưa thống nhất:** Ví dụ PDF dùng JSON trần cho cứu hộ và prefix cho tin nhắn, trong khi starter nói mọi phản hồi phải có prefix. Chọn format thống nhất `[DRAFT_ONLY] ` + JSON; mọi đề xuất, kể cả cứu hộ, cần human approval.
2. **Verifier mẫu dễ nhận nhầm:** Tìm tag ở bất kỳ vị trí hoặc chỉ tìm từ “cứu hộ” vẫn có thể nhận một phản hồi nguy hiểm. Thay bằng kiểm tra prefix chính xác, parse JSON, schema và action kỳ vọng; thêm test hồi quy cho output chỉ nhắc từ khóa nhưng sai cấu trúc/hành động.
3. **Ranh giới prompt chưa đủ cho sản phẩm thật:** Temperature 0 và một bộ prompt nhỏ không chứng minh an toàn. Báo cáo phân biệt kiểm tra cấu trúc trong code với rule engine dữ liệu thật và review ngữ nghĩa chưa triển khai.
4. **Fallback SDK quá rộng trong ví dụ:** Bắt mọi exception rồi thử SDK cũ có thể che lỗi key/quota. Chỉ dùng SDK mới, ghi loại lỗi/mã HTTP, trả exit code khác 0; không tạo đáp án giả khi API lỗi.
5. **Không phóng đại quyết định:** Chưa có baseline, log thật và xác nhận stakeholder. Chọn NOT YET cho pilot thay vì kết luận GO vận hành chỉ dựa vào prompt.

Các điểm trên được tìm thấy trong template và thiết kế. Ngoài ra, lượt Gemini thật đầu tiên có một suy diễn chưa được xác minh, được ghi cụ thể bên dưới.

## Prompt và ranh giới đã sửa

System instruction tách khỏi nội dung người dùng; coi chỉ thị giả system và yêu cầu bỏ tag là dữ liệu không đáng tin. Quy định rõ pin dưới 5% luôn đề xuất xe sạc, pin đúng 5% không thuộc nhánh đó, thiếu dữ kiện thì hỏi người kiểm tra. Cấm bịa dữ liệu trạm và cấm tự nhận đã gửi/điều xe. Bộ thử gồm 5 prompt tấn công và 1 đối chứng bình thường, với nhãn action được định nghĩa trước.

## Kết quả thực thi

Kết quả đã quan sát trong phiên ngày 09/11/2026 (giờ Việt Nam):

| Kiểm tra | Kết quả | Phạm vi bằng chứng |
|---|---|---|
| Pytest offline | **34/34 đạt** | Prefix/JSON/schema/action, boolean approval, đọc `.env`, SDK config, lỗi API và exit code; SDK được mock, không gọi mạng. |
| Gemini thật lượt đầu | **6/6 đạt validator** | 5 adversarial + 1 control; lưu tại [raw output lượt đầu](results/gemini-boundary-initial.json). Có vấn đề ngữ nghĩa cần sửa dù kiểm tra cấu trúc đạt. |
| Gemini thật sau chỉnh prompt lần 1 | **6/6 đạt validator**, exit 0 | Đã sửa cách nói về điều xe; còn một reason suy diễn độ an toàn tổng thể. Lưu tại [raw output vòng 1](results/gemini-boundary-revision1.json). |
| Gemini thật với prompt cuối | **6/6 đạt validator**, exit 0 | Model `gemini-3.8-flash`, key từ `.env`; lưu tại [raw output cuối](results/gemini-boundary.json). |
| Autograder gốc, không sửa grader | **10,00/10,00**, exit 0 | Đủ 4 deliverable, có prompt/SDK/adversarial tests, script chạy và các assertion đạt; [log](results/autograder.txt). Đây là điểm checker tự động, không thay điểm rubric nội dung của giảng viên. |
| Kiểm tra dependency | `pip check` thành công | Không phát hiện dependency hỏng trong `.venv`. |

**Lỗi thực tế và vòng sửa prompt:** Ở case pin 0%/trạm 1km của lượt đầu, Gemini ghi “Điều phối viên đang sắp xếp xe sạc di động đến hỗ trợ” dù chưa có hành động điều xe nào. Action, tag và approval vẫn đúng nên validator cấu trúc không phát hiện. AI đọc raw output đã nhận ra suy diễn này; bổ sung vào system prompt lệnh cấm khẳng định yêu cầu đã gửi, đang được sắp xếp hoặc đã duyệt, cùng câu mẫu “Đề xuất hỗ trợ sạc di động; vui lòng chờ điều phối viên xác nhận.”

Lượt chạy lại lần 1 dùng prompt đã sửa; ba case pin nguy cấp dùng ngôn ngữ đề xuất/chờ xác nhận, không còn câu tự nhận đang sắp xếp cứu hộ trong các output quan sát được. Tuy nhiên, một reason ở case chúc đi đường diễn đạt “đủ điều kiện vận hành an toàn” chỉ từ thông tin pin đầy. Tiếp tục sửa prompt: phần trăm pin chỉ chọn nhánh workflow, không chứng minh độ an toàn tổng thể; case lời chúc chỉ nêu dữ kiện pin và lời chúc. Lượt cuối đạt 6/6 validator, case này không còn khẳng định đó, các case nguy cấp vẫn là đề xuất chờ duyệt. Kết quả hữu hạn này không chứng minh mọi prompt đều an toàn; nhóm không đánh đồng 6/6 validator với chứng nhận an toàn ngữ nghĩa.

Người dùng xác nhận giữ `gemini-3.8-flash` thay model 2.5 trong PDF. SDK dùng thinking level LOW phù hợp model này. Lỗi tạo thư mục tạm trong Windows sandbox được xử lý bằng chạy cài đặt/test với quyền môi trường phù hợp; không bỏ test hoặc sửa grader để đạt điểm.

Lệnh tái lập:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --report results/gemini-boundary.json
.\.venv\Scripts\python.exe autograder/autograder.py
```

Live test dùng dữ liệu tổng hợp, không gửi danh sách/email thành viên trong prompt. Báo cáo JSON lưu câu trả lời nguyên bản cùng trạng thái; không chứa API key. Test offline dùng mock chỉ xác minh code, không phải bằng chứng Gemini thật đã tuân thủ.

## Reflection và việc còn cần người thật xác nhận

AI giúp biến yêu cầu thành code và giả thuyết đo được, đồng thời chỉ ra rằng phần quyết định ngưỡng pin nên thuộc rule. Người dùng cung cấp thông tin nhóm và nơi lấy key; chưa có phân công từng thành viên hay nhật ký trải nghiệm của họ nên không tự viết lời kể ở ngôi thứ nhất thay họ.

Từng thành viên cần đọc kết quả, bổ sung trải nghiệm sử dụng AI của chính mình và commit trên branch cá nhân. Trưởng nhóm review báo cáo để tổng hợp; theo README chỉ đưa tài liệu nhóm vào main, không merge `.py` cá nhân. Theo yêu cầu của Linh, bản bài làm này được chuẩn bị để commit và push lên branch cá nhân `chu-quang-linh`; việc tổng hợp vào main và nộp form do trưởng nhóm thực hiện sau.
