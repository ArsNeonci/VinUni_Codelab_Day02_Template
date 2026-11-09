# Lab 02 — AI Product Scoping

## Phạm vi và nguyên tắc

Tôi sử dụng bốn lăng kính **Lặp lại (Repetitive)**, **Tốn thời gian
(Time-consuming)**, **AI có thể tốt hơn (AI-upgrade)** và **Pain từ người khác
(Stakeholder Pain)** để quét các cơ hội cải tiến vận hành trong hệ sinh thái
Vingroup.

> **Lưu ý về số liệu:** Các mốc thời gian trong tài liệu là baseline giả định
> phục vụ bước sàng lọc ban đầu, không phải số liệu vận hành chính thức. Trước
> khi triển khai, nhóm cần xác minh bằng log hệ thống hoặc phỏng vấn nhân viên
> trực tiếp thực hiện quy trình.

---

# 🔍 Phase 1 — SCAN: Tìm kiếm cơ hội (Cá nhân)

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | **VinFast** | **Lặp lại** | **Phân loại yêu cầu bảo dưỡng/sửa chữa:** Nhân viên phải đọc mô tả, xem ảnh xe, kiểm tra mẫu xe rồi phân loại yêu cầu vào các nhóm như bảo dưỡng, điện–điều hòa, phanh, thân vỏ hoặc lỗi phần mềm trước khi chuyển cho xưởng phù hợp. Tác vụ lặp lại này ước tính mất **3–5 phút/yêu cầu**. AI đa phương thức có thể đề xuất nhóm lỗi, mức ưu tiên và nơi xử lý; nhân viên xác nhận quyết định cuối cùng. |
| 2 | **VinFast** | **Tốn thời gian** | **Tiếp nhận và điều phối cứu hộ pin/Mobile Service:** Nhân viên phải thu thập vị trí, mẫu xe, phần trăm pin, khoảng cách tới trạm sạc và điều kiện tiếp cận hiện trường trước khi chọn phương án hỗ trợ. Tra cứu và tổng hợp thủ công ước tính mất **8–12 phút/trường hợp**. Rule engine kết hợp AI có thể chuẩn hóa thông tin, kiểm tra điều kiện cứu hộ và tạo phương án điều phối dạng nháp. |
| 3 | **Vinmec** | **Pain từ người khác** | **Đối soát thông tin khi kết nối hồ sơ MyVinmec:** Khi họ tên, số điện thoại, ngày sinh hoặc thông tin đăng ký không trùng khớp, người bệnh có thể không thấy lịch hẹn hay hồ sơ y tế. Nhân viên phải kiểm tra và đối soát thủ công, ước tính **10–15 phút/trường hợp**. AI/entity matching có thể phát hiện các bản ghi gần trùng và đề xuất hồ sơ phù hợp; nhân viên bắt buộc xác minh danh tính trước khi liên kết. |
| 4 | **Vinmec** | **Tốn thời gian** | **Soạn bản tóm tắt sau khám/xuất viện:** Bác sĩ hoặc điều dưỡng phải tổng hợp chẩn đoán, thuốc, lịch tái khám, dấu hiệu cảnh báo và hướng dẫn chăm sóc từ nhiều trường dữ liệu. Tác vụ có thể mất khoảng **15–20 phút/bệnh nhân**. LLM có thể tạo bản nháp dễ hiểu từ dữ liệu đã xác thực; bác sĩ phải duyệt và AI không được tự thêm chẩn đoán hay thay đổi đơn thuốc. |
| 5 | **Vinhomes** | **AI-upgrade** | **Phân loại và chuyển phản ánh của cư dân:** Phản ánh dạng văn bản hoặc ảnh về điện nước, thang máy, vệ sinh, an ninh, bãi xe và phí dịch vụ cần được đọc rồi chuyển tới đúng Ban quản lý hoặc nhà thầu. Ticket không rõ hoặc bị trùng có thể làm chậm SLA. AI đa phương thức có thể phân loại, phát hiện trùng, gợi ý mức khẩn cấp và soạn phản hồi xác nhận; không được tự đóng khiếu nại. Baseline giả định: **3–5 phút/ticket**. |
| 6 | **Vinpearl** | **AI-upgrade** | **Hỗ trợ thay đổi lịch trình nghỉ dưỡng:** Khi khách muốn đổi phòng, đổi ngày hoặc thêm dịch vụ, nhân viên phải kiểm tra mã đặt chỗ, chính sách và tình trạng dịch vụ rồi mới tư vấn. Trợ lý AI có kết nối dữ liệu đặt chỗ có thể đề xuất các lựa chọn hợp lệ và tạo lịch trình mới dạng nháp; booking chỉ được cập nhật sau khi khách xác nhận. Baseline giả định: **10–15 phút/yêu cầu**. |
| 7 | **Xanh SM** | **Pain từ người khác** | **Xử lý điểm đón không rõ tại khu đô thị, bệnh viện hoặc trung tâm thương mại:** Tọa độ GPS có thể chỉ vào giữa tòa nhà hoặc sai cổng, khiến tài xế và khách phải gọi nhiều lần để tìm nhau. AI có thể kết hợp tọa độ, tên địa điểm, cổng ra vào, lịch sử điểm đón và mô tả của khách để gợi ý 2–3 điểm đón cụ thể; hệ thống không tự thay đổi điểm đón khi chưa được xác nhận. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards (Cá nhân)

Ba bài toán được chọn để đánh giá nhanh là **#1 VinFast — phân loại yêu cầu
dịch vụ**, **#3 Vinmec — đối soát hồ sơ MyVinmec** và **#5 Vinhomes — phân
luồng phản ánh cư dân**. Cả ba có đầu vào số hóa, tác vụ lặp lại, metric đo được
và có thể giới hạn AI ở vai trò đề xuất để con người kiểm soát quyết định cuối.

## Quick Problem Card #1 — VinFast phân loại yêu cầu dịch vụ

| Trường | Nội dung |
|---|---|
| **Bài toán (1 câu)** | Tự động đọc nội dung và ảnh trong yêu cầu bảo dưỡng/sửa chữa để đề xuất nhóm lỗi, mức ưu tiên và xưởng hoặc đội Mobile Service phù hợp. |
| **Công ty thành viên** | **VinFast** |
| **Ai đang đau (Actor)?** | Cố vấn dịch vụ, nhân viên CSKH, điều phối viên xưởng và khách hàng đang chờ xác nhận lịch. |
| **Workflow thủ công hiện tại (5 bước)** | 1. Khách gửi thông tin xe, mô tả và ảnh lỗi → 2. Nhân viên đọc yêu cầu → 3. Đối chiếu danh mục dịch vụ → 4. Xác định mức ưu tiên và nơi xử lý → 5. Chuyển yêu cầu để xưởng xác nhận lịch. |
| **Bottleneck** | Bước 2–4: nội dung mô tả không đồng nhất, có thể thiếu thông tin hoặc chứa nhiều vấn đề; nhân viên phải đọc ảnh và phân loại lặp lại. Baseline giả định: **3–5 phút/yêu cầu**. |
| **AI có thể hỗ trợ ở đâu?** | OCR/CV và LLM trích xuất mẫu xe, triệu chứng, bộ phận liên quan; đề xuất category, priority, thông tin còn thiếu và nơi xử lý. Nhân viên duyệt hoặc sửa trước khi chuyển yêu cầu. |
| **Metric có số** | (1) Ít nhất **85%** yêu cầu được gợi ý đúng category ở top-1; (2) ít nhất **95%** đúng category trong top-3; (3) giảm thời gian phân loại trung vị từ baseline 3–5 phút xuống **dưới 60 giây**; (4) **0%** yêu cầu an toàn nghiêm trọng được tự động hạ mức ưu tiên mà không qua người duyệt. |
| **Quick Architecture** | **LLM Feature + Computer Vision**, kết hợp rule bắt buộc cho các từ khóa an toàn như phanh, pin quá nhiệt, khói hoặc mất lái. |
| **Operational Boundary** | AI chỉ được đề xuất, không tự chẩn đoán kỹ thuật, báo giá, hứa thời gian hoàn thành hoặc tự xác nhận lịch. Trường hợp confidence thấp hay có dấu hiệu rủi ro phải chuyển người xử lý. |

## Quick Problem Card #3 — Vinmec đối soát hồ sơ MyVinmec

| Trường | Nội dung |
|---|---|
| **Bài toán (1 câu)** | Hỗ trợ phát hiện hồ sơ gần trùng khi thông tin đăng ký MyVinmec không khớp hoàn toàn với dữ liệu bệnh viện, giúp nhân viên đối soát nhanh và an toàn hơn. |
| **Công ty thành viên** | **Vinmec** |
| **Ai đang đau (Actor)?** | Người bệnh không xem được lịch hẹn/hồ sơ; nhân viên tiếp đón và CSKH phải dò tìm, gọi xác minh và sửa thông tin thủ công. |
| **Workflow thủ công hiện tại (5 bước)** | 1. Người bệnh báo không kết nối được hồ sơ → 2. Nhân viên thu thập thông tin định danh → 3. Tìm kiếm trong hệ thống → 4. So sánh các trường bị lệch và xác minh với người bệnh → 5. Nhân viên có thẩm quyền liên kết hoặc cập nhật hồ sơ. |
| **Bottleneck** | Bước 3–4: lỗi chính tả, dấu tiếng Việt, đổi số điện thoại hoặc đảo thứ tự họ tên làm kết quả tìm kiếm chính xác thất bại. Baseline giả định: **10–15 phút/trường hợp**. |
| **AI có thể hỗ trợ ở đâu?** | Chuẩn hóa tên/địa chỉ, fuzzy matching và mô hình entity resolution tạo danh sách ứng viên kèm lý do, trường khớp và điểm tin cậy; nhân viên thực hiện xác minh đa yếu tố trước khi liên kết. |
| **Metric có số** | (1) Hồ sơ đúng xuất hiện trong top-3 ở ít nhất **95%** bộ dữ liệu kiểm thử; (2) giảm thời gian đối soát trung vị xuống **dưới 3 phút**; (3) tỷ lệ liên kết nhầm sau xác minh bằng **0%**; (4) **100%** thao tác xem/gợi ý/liên kết được ghi audit log. |
| **Quick Architecture** | **Rule + ML/entity matching**; không cần Agent tự trị. Rule xử lý các trường định danh cứng, mô hình similarity chỉ xếp hạng ứng viên. |
| **Operational Boundary** | AI không được tự liên kết, gộp, xóa hoặc sửa hồ sơ y tế. Không hiển thị dữ liệu nhạy cảm vượt quá quyền của nhân viên. Mọi liên kết phải qua xác minh danh tính và phê duyệt của người có thẩm quyền. |

## Quick Problem Card #5 — Vinhomes phân luồng phản ánh cư dân

| Trường | Nội dung |
|---|---|
| **Bài toán (1 câu)** | Tự động phân loại phản ánh văn bản/ảnh của cư dân, phát hiện ticket trùng và đề xuất đơn vị xử lý cùng mức ưu tiên. |
| **Công ty thành viên** | **Vinhomes** |
| **Ai đang đau (Actor)?** | Cư dân chờ phản hồi; nhân viên Ban quản lý phải đọc, phân loại và chuyển ticket; đội kỹ thuật hoặc nhà thầu nhận sai/thiếu thông tin. |
| **Workflow thủ công hiện tại (5 bước)** | 1. Cư dân gửi phản ánh và ảnh → 2. CSKH đọc nội dung → 3. Phân loại lĩnh vực và mức độ → 4. Kiểm tra ticket trùng rồi chuyển bộ phận/nhà thầu → 5. Gửi phản hồi xác nhận cho cư dân. |
| **Bottleneck** | Bước 2–4: mô tả tự do, ảnh thiếu ngữ cảnh và ticket lặp khiến việc route sai hoặc phải chuyển lại. Baseline giả định: **3–5 phút/ticket**. |
| **AI có thể hỗ trợ ở đâu?** | LLM + Vision trích xuất tòa/căn/khu vực, loại sự cố và mức khẩn cấp; semantic search tìm ticket tương tự; hệ thống đề xuất đội xử lý và soạn phản hồi xác nhận dạng nháp. |
| **Metric có số** | (1) Ít nhất **90%** ticket được route đúng ngay lần đầu; (2) ít nhất **85%** ticket trùng được phát hiện; (3) giảm thời gian phân loại trung vị xuống **dưới 30 giây**; (4) **100%** ticket an ninh, cháy, điện giật hoặc kẹt thang máy được chuyển hàng đợi khẩn cấp và báo người trực. |
| **Quick Architecture** | **LLM Feature + Vision + semantic search**, kết hợp rule ưu tiên khẩn cấp. Không dùng Agent tự trị để tự đóng ticket hoặc điều động nhà thầu. |
| **Operational Boundary** | AI không tự kết luận trách nhiệm, cam kết bồi thường, đóng khiếu nại hoặc gửi dữ liệu cư dân cho nhà thầu ngoài phạm vi cần thiết. Ticket khẩn cấp và ticket confidence thấp phải được người trực xác nhận. |
