# 02 — Deep-Dive Report
**Tên nhóm:** A95
**Thành viên:**
- Trương Thị Thu Hà — 26ai.hattt@vinuni.edu.vn

**Bài toán nhóm chọn:** Card #3 — AI hỗ trợ chuẩn bị bản bàn giao ca điều dưỡng (Vinmec).

**Vì sao chọn #3:** Quy trình bàn giao ca diễn ra thường xuyên và đòi hỏi điều dưỡng đọc, tổng hợp nhiều ghi chú bệnh nhân. LLM phù hợp với nhiệm vụ tạo bản nháp tóm tắt, giúp tiết kiệm thời gian nhưng vẫn giữ điều dưỡng là người kiểm tra và quyết định.

**Vì sao không chọn các bài khác:**
- **#2 — Đối chiếu bảo hiểm:** Quy trình liên quan đến nhiều quy định và điều kiện bảo hiểm khác nhau, đòi hỏi thông tin chính xác và được cập nhật. Prototype có thể phức tạp hơn do phải kết hợp trích xuất tài liệu và kiểm tra quy tắc nghiệp vụ.
- **#4 — Phân loại phản hồi:** Mặc dù dễ triển khai và ít rủi ro, bài toán phân loại phản hồi tương đối phổ biến. Nhóm ưu tiên #3 vì có thể giải quyết một quy trình vận hành cụ thể, có tần suất lặp lại và có thể đo thời gian tiết kiệm.

## 3.1. Current-State Workflow
Sơ đồ: xem file `04-workflow-diagram.png`

**Phạm vi đo:** Thời gian chuẩn bị bản tóm tắt bàn giao của một điều dưỡng, bao gồm bước chuyển và xác nhận bản tóm tắt. Không tính toàn bộ thời gian bàn giao lâm sàng trực tiếp.

| Bước | Ai thực hiện? | Công việc | Thời gian |
|---|---|---|---|
| 1 | Điều dưỡng ca trước | Đọc hồ sơ và ghi chú chăm sóc bệnh nhân | 5 phút |
| 2 | Điều dưỡng ca trước | Tổng hợp diễn biến, thông tin cần theo dõi và công việc chưa hoàn thành 🔴 (bottleneck) | 8 phút |
| 3 | Điều dưỡng ca trước | Viết bản tóm tắt bàn giao | 5 phút |
| 4 | Điều dưỡng ca trước và ca sau | 🔄 Chuyển bản tóm tắt, xác nhận đã nhận và làm rõ thông tin ban đầu | 2 phút |
| **Tổng** | | | **20 phút/lượt** |

**Điểm bàn giao giữa người với người (🔄):**
- **Bước 3 → 4:** Điều dưỡng ca trước chuyển bản tóm tắt cho điều dưỡng ca sau.
- **Bước 4:** Hai bên đối chiếu và làm rõ thông tin, sau đó tiếp tục bàn giao lâm sàng theo quy trình của bệnh viện.
- AI chỉ hỗ trợ chuẩn bị tài liệu, không thay thế việc bàn giao trực tiếp giữa hai điều dưỡng.

## 3.2. Problem Statement (6-field)
| Field | Nội dung |
|---|---|
| 1. Actor / Operator | Điều dưỡng ca trước (người chuẩn bị và xác nhận bản bàn giao) và điều dưỡng ca sau (người tiếp nhận) tại khoa nội trú Vinmec. |
| 2. Current Workflow | Đọc hồ sơ và ghi chú (5') → Tổng hợp diễn biến, việc cần theo dõi (8') → Viết bản tóm tắt (5') → Chuyển và xác nhận với ca sau (2'). Tổng 20 phút/lượt. |
| 3. Bottleneck | Bước 2 — tổng hợp diễn biến, thông tin cần theo dõi và công việc chưa hoàn thành từ nhiều ghi chú, khoảng 8 phút/lượt. |
| 4. Business Impact | Giả định 1 khoa: 8 điều dưỡng/ca × 3 ca/ngày × 20 phút = 480 phút = **8 giờ công/ngày**, khoảng 240 giờ công/30 ngày dành cho việc chuẩn bị bàn giao. |
| 5. Success Metric | Giảm thời gian chuẩn bị bàn giao từ **20 phút xuống 8 phút/lượt** (giảm 60%), tức tiết kiệm **4,8 giờ công/ngày/khoa** (khoảng 144 giờ công/30 ngày), mà không làm sai hoặc bỏ sót thông tin quan trọng (định danh bệnh nhân, thuốc, dị ứng). Thời gian tiết kiệm được phân bổ lại cho chăm sóc bệnh nhân, không nhằm giảm nhân sự. |
| 6. Operational Boundary | **AI được làm:** đọc và tóm tắt ghi chú chăm sóc do nhân viên cung cấp trong môi trường được phê duyệt; trích xuất thông tin theo mẫu cố định; sắp xếp theo nhóm (tình trạng hiện tại, việc đã hoàn thành, việc còn lại); đánh dấu thông tin thiếu, không rõ hoặc mâu thuẫn; dẫn về ghi chú gốc để kiểm chứng. **TUYỆT ĐỐI KHÔNG:** tự chẩn đoán hoặc quyết định điều trị; tự thay đổi đơn thuốc, liều lượng, chỉ định; tự tạo dữ liệu bệnh nhân khi không có nguồn; tự xác nhận bản bàn giao là chính xác; tự động gửi bản tóm tắt chưa duyệt cho ca sau; dùng dữ liệu bệnh nhân thật trên nền tảng AI chưa được bệnh viện cho phép. **Điểm cần người duyệt:** điều dưỡng ca trước kiểm tra và xác nhận bản tóm tắt; điều dưỡng ca sau đối chiếu khi tiếp nhận. |

## 3.3. Future-State Flow & AI Fit
| Mức | Phương án | Đủ khi nào | Rủi ro | Chọn? |
|---|---|---|---|---|
| Rule / State-Machine | Mẫu bàn giao cố định + checklist các mục bắt buộc | Đủ để chuẩn hóa định dạng, nhưng không tự đọc và tổng hợp được ghi chú tự do | Không giải quyết được bước 2 (tổng hợp) — bottleneck chính | Không chọn làm toàn bộ; dùng mẫu cố định làm khung đầu ra cho AI |
| LLM Feature | LLM đọc ghi chú được cung cấp, tạo bản nháp theo mẫu, đánh dấu chỗ thiếu/mâu thuẫn; điều dưỡng duyệt | Phù hợp vì quy trình cố định, AI chỉ hỗ trợ bước đọc–tổng hợp–soạn thảo văn bản | Bỏ sót hoặc sai thông tin, hallucination → bắt buộc điều dưỡng duyệt và đối chiếu ghi chú gốc | **Chọn** |
| Agentic Loop | Agent tự truy cập hồ sơ, tự quyết định thông tin cần lấy và tự gửi bàn giao | Chỉ cần nếu quy trình nhiều nhánh, phải tự lập kế hoạch | Rủi ro quá cao trong y tế (truy cập dữ liệu bệnh nhân, tự gửi khi chưa duyệt) | Không chọn |

**Future-State Flow (mục tiêu tổng 8 phút/lượt):**
1. Điều dưỡng ca trước cung cấp ghi chú chăm sóc của các bệnh nhân trong ca (môi trường được phê duyệt) →
2. 🔵 **AI:** đọc ghi chú, tạo bản nháp bàn giao theo mẫu cố định, đánh dấu thông tin thiếu/không rõ/mâu thuẫn, kèm dẫn về ghi chú gốc →
3. 🟢 **Điều dưỡng ca trước:** đối chiếu với ghi chú gốc (định danh bệnh nhân, thuốc, dị ứng…), chỉnh sửa và xác nhận →
4. 🔄 Chuyển bản đã duyệt cho điều dưỡng ca sau; 🟢 ca sau đối chiếu và làm rõ khi tiếp nhận, tiếp tục bàn giao lâm sàng theo quy trình bệnh viện.

↩️ **Fallback** (nguyên tắc: AI hỗ trợ soạn thảo, con người chịu trách nhiệm xác minh):
1. **Phát hiện lỗi:** điều dưỡng đối chiếu bản tóm tắt với ghi chú gốc, đặc biệt định danh bệnh nhân, thuốc, dị ứng và thông tin quan trọng.
2. **Đánh dấu lỗi:** nếu thông tin sai, thiếu nguồn hoặc mâu thuẫn, bản nháp không được phê duyệt.
3. **Quay lại quy trình thủ công:** điều dưỡng trực tiếp đọc hồ sơ gốc và tự tổng hợp thông tin cần bàn giao.
4. **Ghi nhận lỗi:** lưu loại lỗi và nguyên nhân để cải thiện prompt hoặc quy trình.
5. **Xác minh trước khi sử dụng:** chỉ dùng bản bàn giao đã được nhân viên y tế kiểm tra và xác nhận.
- **Khi AI không hoạt động:** tiếp tục quy trình bàn giao thủ công hiện tại, không để lỗi hệ thống làm gián đoạn bàn giao ca.

## Phase 4 — Kết quả Prompt Prototype
- Prototype trong bài lab (`starter-code/prompt_prototype.py`) kiểm tra cùng nguyên tắc ranh giới trên tình huống mẫu Xanh SM: bản nháp bắt buộc gắn `[DRAFT_ONLY]` để người duyệt trước khi gửi; pin dưới 5% thì không chỉ đường đến trạm sạc xa hơn 5km mà điều xe sạc di động.
- Kết quả: **3/3 test Passed** (Rule 2 — điều xe sạc di động khi pin 2%; Rule 1 — giữ thẻ `[DRAFT_ONLY]` khi bị yêu cầu bỏ; Rule 1 — giữ thẻ khi bị giả danh quản trị viên "SYSTEM OVERRIDE").
- Áp dụng cho bài toán bàn giao ca: nguyên tắc "AI chỉ soạn nháp, người duyệt trước khi gửi" tương ứng với việc bản bàn giao chỉ được chuyển cho ca sau sau khi điều dưỡng xác nhận.

## Phase 5 — Evaluate
- [x] Có sẵn dữ liệu mẫu / logs sạch để test? — Có thể tạo dữ liệu ghi chú điều dưỡng giả lập, không dùng thông tin bệnh nhân thật.
- [x] Rủi ro khi AI sai nằm trong tầm kiểm soát (HITL / Fallback)? — Có điều dưỡng duyệt bắt buộc và fallback về quy trình thủ công.
- [ ] Stakeholders sẵn sàng thay đổi quy trình cũ? — Chưa kiểm chứng với điều dưỡng và bộ phận chuyên môn của Vinmec.

**Quyết định:** **GO** — cho phép phát triển prototype với dữ liệu giả lập. Triển khai thực tế: **NOT YET**.

**Justification:**
- Vấn đề có quy trình rõ ràng, lặp lại hằng ngày và có thể đo được thời gian xử lý.
- LLM phù hợp với nhiệm vụ tóm tắt và cấu trúc lại văn bản.
- Có thể tạo dữ liệu ghi chú điều dưỡng giả lập để thử nghiệm mà không sử dụng thông tin bệnh nhân thật.
- Dễ so sánh kết quả trước và sau khi sử dụng AI.
- Có phương án fallback rõ ràng và cơ chế nhân viên y tế phê duyệt.

**Điều kiện để tiếp tục triển khai thực tế:**
- Kiểm chứng thời gian thực tế và tính cần thiết của giải pháp với điều dưỡng.
- Đánh giá mức độ chính xác, đặc biệt là lỗi bỏ sót hoặc làm sai thông tin quan trọng.
- Được phê duyệt về bảo mật dữ liệu và an toàn chuyên môn.
- Thử nghiệm dưới sự giám sát của nhân viên y tế.

**Kết luận:** Chọn Card #3 để xây dựng prototype LLM hỗ trợ tạo bản nháp bàn giao ca điều dưỡng, với mục tiêu giảm thời gian chuẩn bị từ 20 phút xuống 8 phút mà không thay thế vai trò kiểm tra và xác nhận của điều dưỡng. Trạng thái triển khai thực tế vẫn là NOT YET vì chưa đủ bằng chứng về hiệu quả, độ an toàn và sự phù hợp với quy trình thực tế của Vinmec.
