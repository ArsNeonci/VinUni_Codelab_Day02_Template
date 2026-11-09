# Nhật ký sử dụng AI — Lab 02

## AI hỗ trợ quá trình phân tích

Tôi sử dụng AI để trao đổi ý tưởng, hỗ trợ phân tích và rà soát phương án cho bài toán làm rõ điểm đón khách của Xanh SM. Những gợi ý hữu ích tập trung vào cách xác định thông tin còn thiếu, xử lý dữ liệu mâu thuẫn và phân chia vai trò giữa quy tắc, LLM và điều phối viên. AI cũng hỗ trợ xây dựng prompt và các tình huống thử gây áp lực để mô hình tự đoán điểm đón hoặc bỏ bước duyệt.

## Điểm cần kiểm chứng và điều chỉnh

Các mức thời gian 4 phút và mục tiêu 1,5 phút được dùng để minh họa thiết kế đánh giá. Chúng cần được xác nhận bằng dữ liệu vận hành trước khi dùng để kết luận về hiệu quả. Tôi cũng cần phân biệt kết quả mong đợi của một ca thử với phản hồi thực tế của mô hình.

Khi rà soát bản mẫu, một điểm chưa phù hợp là prompt và dữ liệu test đã chuyển sang bài toán điểm đón nhưng phần kiểm tra vẫn tìm từ khóa cứu hộ pin. Ngoài ra, việc tìm thấy nhãn `[DRAFT_ONLY]` trong phản hồi chưa đủ để kết luận mô hình tuân thủ yêu cầu. Cần kiểm tra vị trí nhãn, cấu trúc JSON và nội dung trả lời của từng ca.

## Cách làm rõ yêu cầu và ranh giới

Qua việc yêu cầu chỉnh prompt và test cho đúng đề tài, phạm vi xử lý được cụ thể hóa thành trích xuất thông tin có trong đầu vào và soạn bản nháp chờ duyệt. Trường thiếu phải để trống và được hỏi lại. Khi thông tin đặt xe ghi cổng A nhưng khách nói cổng B, mô hình cần nêu mâu thuẫn và xin xác nhận. Điều phối viên duyệt câu hỏi trước khi gửi, khách xác nhận điểm đón trước khi chuyển thông tin cho tài xế.

Từ quá trình này, tôi thấy cần đánh giá cả nội dung AI trả lời và cách chương trình kiểm tra nội dung đó. Prompt rõ ràng, đáp án kỳ vọng cụ thể và kiểm thử phù hợp là cơ sở để đánh giá khả năng giữ ranh giới. Hiệu quả thực tế vẫn cần được xác nhận bằng kết quả chạy thử và số liệu đo.
