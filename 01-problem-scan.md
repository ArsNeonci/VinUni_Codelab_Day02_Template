# Phần cá nhân — Quét cơ hội và đánh giá nhanh 3 bài toán

## Phase 1 — Danh sách 5 bài toán

Bảng sử dụng đủ bốn góc nhìn của worksheet, gồm tác vụ lặp lại, tác vụ tốn thời gian, cơ hội AI cải thiện cách xử lý và khó khăn của người liên quan.

| #   | Đơn vị   | Góc nhìn                    | Bài toán                                                                                                     |
| --- | -------- | --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| 1   | Xanh SM  | Tốn thời gian               | Điều phối viên phải đọc mô tả điểm đón chưa rõ của khách, hỏi bổ sung và soạn thông tin xác nhận cho tài xế. |
| 2   | VinFast  | Lặp lại                     | Nhân viên đối soát phải so khớp phiên sạc với dòng hóa đơn và tách giao dịch lệch để rà soát.                |
| 3   | Vinhomes | AI có thể hỗ trợ tốt hơn    | Phản ánh tự do của cư dân có thể thiếu thông tin hoặc bị chuyển nhầm đội xử lý.                              |
| 4   | Vinpearl | Tốn thời gian               | Nhân viên đặt phòng phải tách ngày ở, số khách và yêu cầu đặc biệt từ email đặt theo đoàn.                   |
| 5   | Xanh SM  | Khó khăn của người vận hành | Tài xế ghi lý do hủy chuyến bằng nhiều cách, khiến nhân viên khó tổng hợp nguyên nhân theo tuần.             |

## Phase 2 — Ba thẻ đánh giá nhanh

### Thẻ 1 — Xanh SM làm rõ điểm đón khách

```less
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Mô tả điểm đón thiếu tên cổng, phía đường hoặc    │
│   mốc nhận diện khiến khách và tài xế phải trao đổi nhiều   │
│   lần.                                                      │
│ Công ty thành viên: [x] Xanh SM (GSM)                       │
│                                                             │
│ Ai đang đau? Điều phối viên, tài xế tìm điểm đón và khách   │
│   đang chờ xe.                                              │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Nhận mô tả điểm đón từ khách                           │
│   → 2. Đối chiếu thông tin đặt xe                           │
│   → 3. Xác định thông tin thiếu hoặc mâu thuẫn              │
│   → 4. Hỏi khách bổ sung thông tin                          │
│   → 5. Soạn và xác nhận điểm đón với tài xế                 │
│                                                             │
│ Bước nào tốn nhất? Đọc, đối chiếu và soạn câu hỏi ở bước    │
│   1–4 (giả định 4 phút/yêu cầu, chưa tính chờ khách trả     │
│   lời).                                                     │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 1–4.             │
│ (Trích xuất địa điểm, cổng, mốc nhận diện → phát hiện       │
│   trường thiếu → soạn câu hỏi để người duyệt.)              │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Trên 30 yêu cầu giả lập, giảm trung vị thời gian từ nhận    │
│   yêu cầu đến duyệt câu hỏi từ 4 phút xuống tối đa 1,5      │
│   phút.                                                     │
│ Ít nhất 27/30 đầu ra khớp đáp án. Cả 10 ca thiếu hoặc mâu   │
│   thuẫn phải được đánh dấu cần làm rõ.                      │
│                                                             │
│ Quick Architecture: [x] LLM Feature [x] Rule                │
│ (Trích xuất và soạn bản nháp, kiểm tra trường thông tin.)   │
└─────────────────────────────────────────────────────────────┘
```

- **Dữ liệu cần xác nhận** — Mô tả điểm đón và thông tin đặt xe đã ẩn danh, cùng thời gian xử lý cơ sở. Bài lab dùng 30 yêu cầu giả lập có đáp án xác nhận trường nào có dữ liệu và trường nào cần hỏi lại.
- **Ranh giới dự kiến** — Thông tin điểm đón phải có căn cứ từ dữ liệu khách cung cấp. Trường chưa rõ được để trống và hỏi lại. Điều phối viên duyệt bản nháp, khách xác nhận điểm đón trước khi cập nhật cho tài xế.

### Thẻ 2 — VinFast đối soát hóa đơn sạc

```less
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Nhân viên phải tìm thủ công giao dịch có số tiền  │
│   hoặc thông tin phiên sạc không khớp hóa đơn.              │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau? Nhân viên đối soát thanh toán.                 │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Tải dữ liệu phiên sạc                                  │
│   → 2. Chuẩn hóa mã giao dịch                               │
│   → 3. So khớp hóa đơn và tách dòng chênh lệch              │
│   → 4. Gửi danh sách chênh lệch để duyệt                    │
│                                                             │
│ Bước nào tốn nhất? Bước 3 (giả định 30 phút/lô).            │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3 có thể tự động │
│   hóa bằng Rule.                                            │
│ (So khớp mã phiên → đánh dấu chênh lệch theo ngưỡng → nhân  │
│   viên kiểm tra mã thiếu hoặc trùng.)                       │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian rà một lô giả lập 100 dòng từ 30 phút xuống  │
│   tối đa 10 phút. Phát hiện đủ 10 dòng lệch đã cài sẵn.     │
│                                                             │
│ Quick Architecture: [x] Rule [ ] LLM [ ] Agent              │
│ (So khớp dữ liệu theo mã phiên và ngưỡng sai số.)           │
└─────────────────────────────────────────────────────────────┘
```

- **Dữ liệu cần xác nhận** — Hai bảng có mã phiên, thời gian và số tiền, cùng quy định về sai số cho phép. Dùng bộ giả lập 100 dòng có đáp án đối soát để đo thời gian và số dòng lệch phát hiện được.
- **Ranh giới dự kiến** — Hệ thống tạo danh sách cần kiểm tra. Nhân viên xác nhận trước khi điều chỉnh hoặc thanh toán.

### Thẻ 3 — Vinhomes phân loại phản ánh cư dân

```less
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Nhân viên phải đọc phản ánh viết tự do, tìm thông │
│   tin còn thiếu và chọn đội phụ trách.                      │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? Nhân viên tiếp nhận phản ánh và cư dân chờ     │
│   được hỗ trợ.                                              │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Nhận phản ánh của cư dân                               │
│   → 2. Đọc và xác định loại sự cố                           │
│   → 3. Hỏi lại nếu thiếu thông tin                          │
│   → 4. Chuyển đội phụ trách                                 │
│                                                             │
│ Bước nào tốn nhất? Bước 2 (giả định 5 phút/phiếu).          │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2–3.             │
│ (Gợi ý nhãn theo danh mục → chỉ ra thông tin thiếu → nhân   │
│   viên xác nhận đội tiếp nhận.)                             │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Gợi ý đúng đội cho ít nhất 90% trong bộ 50 phiếu đã gắn     │
│   nhãn. Thời gian duyệt trung vị tối đa 2 phút/phiếu.       │
│                                                             │
│ Quick Architecture: [x] LLM Feature                         │
│ (Gợi ý phân loại, con người xác nhận.)                      │
└─────────────────────────────────────────────────────────────┘
```

- **Dữ liệu cần xác nhận** — Danh mục sự cố, đội phụ trách và 50 phiếu đã ẩn danh, được người vận hành gắn nhãn. So sánh nhãn AI đề xuất với nhãn đã duyệt và ghi thời gian duyệt từng phiếu.
- **Ranh giới dự kiến** — Nhân viên quyết định phân tuyến. Phiếu thiếu thông tin hoặc có nhiều loại sự cố được chuyển để kiểm tra thủ công.

## Đề xuất cá nhân để thảo luận nhóm

Ba thẻ được chọn vì đại diện cho ba kiểu công việc có thể thử nghiệm bằng dữ liệu giả lập, gồm trích xuất và làm rõ thông tin, đối soát dữ liệu và phân loại văn bản.

| Bài toán                      | Điểm thuận lợi khi thử nghiệm                                                     | Điều cần làm rõ                                                                         |
| ----------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Xanh SM — Làm rõ điểm đón     | Có thể kiểm thử việc trích xuất thông tin, phát hiện trường thiếu và soạn câu hỏi | Các trường thông tin cần thiết, thời gian xử lý cơ sở và cách xác nhận điểm đón thực tế |
| VinFast — Đối soát hóa đơn    | Có thể tạo bộ dữ liệu với kết quả đúng biết trước                                 | Khả năng giải quyết đầy đủ bằng quy tắc so khớp                                         |
| Vinhomes — Phân loại phản ánh | Có thể đo độ chính xác bằng phiếu được gắn nhãn                                   | Danh mục phân tuyến và chất lượng nhãn do người vận hành cung cấp                       |

Đề xuất ưu tiên thẻ 1 để nhóm xem xét vì phạm vi có thể giới hạn ở trích xuất thông tin và hỏi lại, với đầu ra kiểm tra được bằng bộ đáp án giả lập. Nhóm sẽ đối chiếu các đề xuất của từng thành viên rồi thống nhất bài toán cho phần phân tích sâu.
