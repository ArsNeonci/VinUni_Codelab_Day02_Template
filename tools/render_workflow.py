"""A95 - render the GROUP workflow, keeping the shared report scope and timings.
Chu Quang Linh <Quanglinh1286@gmail.com>; Nguyễn Minh Quân <minhquandhtb@gmail.com>;
Trương Thu Hà <thuha261102@gmail.com>; Phan Trần Mạnh Cường <manhcuong2005.28@gmail.com>;
Nguyễn Lương Phúc <luongphuc.lpu@gmail.com>.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def main():
    im = Image.new("RGB", (2400, 1800), "#f3f6fa")
    d = ImageDraw.Draw(im)
    fonts = Path("C:/Windows/Fonts")
    ink, muted = "#17243b", "#53647b"
    red, blue, green, orange, slate = "#b33444", "#246faa", "#237962", "#b96a1b", "#5a6e87"

    def font(size, bold=False):
        return ImageFont.truetype(str(fonts / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)

    def wrap(text, x, y, width, face, fill=ink, step=34):
        lines, line = [], ""
        for word in text.split():
            cand = (line + " " + word).strip()
            if line and d.textlength(cand, font=face) > width:
                lines.append(line)
                line = word
            else:
                line = cand
        lines.append(line)
        for line in lines:
            d.text((x, y), line, font=face, fill=fill)
            y += step
        return y

    def arrow(x1, y1, x2, y2, color=slate, width=4):
        d.line((x1, y1, x2, y2), fill=color, width=width)
        if x2 > x1:
            points = [(x2, y2), (x2-12, y2-9), (x2-12, y2+9)]
        elif y2 > y1:
            points = [(x2, y2), (x2-9, y2-12), (x2+9, y2-12)]
        else:
            points = [(x2, y2), (x2-9, y2+12), (x2+9, y2+12)]
        d.polygon(points, fill=color)

    d.rectangle((0, 0, 2400, 105), fill=ink)
    d.text((70, 22), "A95 | DISCHARGE SUMMARY - WORKFLOW NHÓM", font=font(47, True), fill="white")
    members = [
        "Chu Quang Linh | Quanglinh1286@gmail.com     •     Nguyễn Minh Quân | minhquandhtb@gmail.com",
        "Trương Thu Hà | thuha261102@gmail.com     •     Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com",
        "Nguyễn Lương Phúc | luongphuc.lpu@gmail.com",
    ]
    for i, line in enumerate(members):
        d.text((70, 122+i*35), line, font=font(25), fill=muted)
    d.rounded_rectangle((70, 250, 2330, 325), radius=15, fill="#dce8f4")
    d.text((90, 266), "GIẢ ĐỊNH CHO LAB • Đo từ mở nguồn sau quyết định xuất viện đến xong rà nháp; chưa đo tại Vinmec.", font=font(29, True), fill=blue)

    current = [
        ("C1", "Tập hợp đúng nguồn", "Bác sĩ • EHR / ghi chép", "ID người / đợt điều trị → tập nguồn", "3 phút", slate),
        ("C2", "Rà diễn biến và xét nghiệm", "Bác sĩ • nhiều nguồn", "Ghi chép → diễn biến / kết quả chờ", "5 phút", red),
        ("C3", "Đối chiếu dữ kiện và đơn", "Bác sĩ • hỏi lại khi cần", "Nguồn → thuốc / dị ứng / tái khám", "6 phút", red),
        ("C4", "Soạn bản nháp theo mục", "Bác sĩ • mẫu tóm tắt", "Thông tin đã đối chiếu → nháp", "4 phút", slate),
        ("C5", "Bác sĩ rà lại bản nháp", "Bác sĩ • nguồn đối chiếu", "Nháp → bản đã được rà soát", "2 phút", green),
    ]
    future = [
        ("F1", "Chuẩn bị và kiểm tra nguồn", "HUMAN • đúng người / đợt", "Chỉ nguồn đã được phép dùng", "3 phút", green),
        ("F2", "Điền template và mục thiếu", "RULE • không cần LLM", "Giữ nguyên dữ kiện có cấu trúc", "1 phút", slate),
        ("F3", "Nháp AI tùy chọn + kiểm tra", "AI / RULE • sandbox", "Template đủ thì bỏ lời gọi AI", "1 phút", blue),
        ("F4", "Bác sĩ đối chiếu và sửa", "HUMAN-IN-THE-LOOP", "Thiếu / mâu thuẫn phải làm rõ", "6 phút", green),
        ("F5", "Hoàn tất bản nháp", "HUMAN • chưa tự phát hành", "Chuyển tiếp quy trình chuyên môn", "1 phút", green),
    ]

    def row(items, y):
        for i, (num, title, actor, flow, time, color) in enumerate(items):
            x = 70+i*460
            d.rounded_rectangle((x, y, x+420, y+300), radius=20, fill="white", outline=color, width=4)
            d.rounded_rectangle((x+20, y+17, x+91, y+60), radius=9, fill=color)
            d.text((x+31, y+20), num, font=font(27, True), fill="white")
            wrap(title, x+20, y+78, 380, font(29, True), step=36)
            wrap(actor, x+20, y+160, 380, font(23), muted, step=29)
            wrap(flow, x+20, y+205, 380, font(23), ink, step=29)
            d.text((x+20, y+258), time, font=font(29, True), fill=color)
            if i < 4:
                arrow(x+423, y+150, x+452, y+150)

    d.text((70, 355), "CURRENT STATE | 20 phút giả định • Bottleneck C2 + C3 = 11 phút", font=font(35, True), fill=ink)
    row(current, 420)
    wrap("H1: EHR / ghi chép → bác sĩ   |   H2: bác sĩ ↔ người phụ trách nguồn khi cần làm rõ   |   H3: sau rà nháp → quy trình ký / bàn giao", 70, 755, 2260, font(27), blue, 35)
    d.text((70, 860), "FUTURE STATE | Mục tiêu 12 phút • Template-first, LLM chỉ thử khi có giá trị thêm", font=font(35, True), fill=ink)
    row(future, 930)
    arrow(1200, 1233, 1200, 1315, orange)
    arrow(1660, 1315, 1660, 1233, orange)
    d.text((780, 1260), "Lỗi / không đủ căn cứ", font=font(25, True), fill=orange)
    d.text((1668, 1260), "Soạn thủ công", font=font(25, True), fill=orange)
    d.rounded_rectangle((880, 1320, 1890, 1460), radius=18, fill="#fff1df", outline=orange, width=3)
    d.text((905, 1334), "FALLBACK: chặn nháp AI; không giả báo test đạt", font=font(28, True), fill=orange)
    wrap("Giữ template đã đối chiếu nếu có; bác sĩ đọc nguồn và tự soạn. Không tự sửa phản hồi lỗi thành thành công.", 905, 1384, 960, font(25), ink, 32)
    d.rounded_rectangle((70, 1520, 2330, 1605), radius=15, fill=ink)
    d.text((90, 1535), "NGOÀI PHẠM VI ĐO: quyết định xuất viện • chờ ký • thanh toán / bảo hiểm • thời điểm người bệnh rời viện", font=font(28, True), fill="white")
    d.text((90, 1570), "AI không tự kê đơn, ký, gửi hoặc ghi EHR. Nháp giả lập chưa phải tài liệu sử dụng cho người bệnh.", font=font(25), fill="#d5e2ef")
    legend = [(red, "Bottleneck"), (slate, "Rule / nguồn"), (blue, "AI thử nghiệm"), (green, "Người duyệt"), (orange, "Fallback")]
    for i, (color, label) in enumerate(legend):
        x = 70+i*450
        d.rounded_rectangle((x, 1655, x+28, 1683), radius=5, fill=color)
        d.text((x+42, 1652), label, font=font(25, True), fill=ink)
    d.text((70, 1728), "Các mốc thời gian là mục tiêu / giả định. 8/8 fixture không phải đánh giá lâm sàng. Quyết định: NOT YET cho triển khai LLM.", font=font(26), fill=muted)
    im.save(ROOT / "04-workflow-diagram.png")
    print("Rendered group workflow: 04-workflow-diagram.png")


if __name__ == "__main__":
    main()
