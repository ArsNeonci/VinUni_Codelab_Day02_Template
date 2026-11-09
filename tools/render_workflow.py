"""Nhóm A95 - reproducible current-state workflow PNG (Pillow).
Chu Quang Linh <Quanglinh1286@gmail.com>; Nguyễn Minh Quân <minhquandhtb@gmail.com>;
Trương Thu Hà <thuha261102@gmail.com>; Phan Trần Mạnh Cường <manhcuong2005.28@gmail.com>;
Nguyễn Lương Phúc <luongphuc.lpu@gmail.com>.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path("C:/Windows/Fonts")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)


def wrap(draw, text, xy, width, typeface, fill, line_height):
    x, y = xy
    line = ""
    for word in text.split():
        next_line = (line + " " + word).strip()
        if line and draw.textlength(next_line, font=typeface) > width:
            draw.text((x, y), line, font=typeface, fill=fill)
            y += line_height
            line = word
        else:
            line = next_line
    draw.text((x, y), line, font=typeface, fill=fill)
    return y + line_height


def main():
    image = Image.new("RGB", (1800, 1590), "#f3f6fa")
    draw = ImageDraw.Draw(image)
    ink, muted, blue, red = "#17243b", "#526178", "#216baf", "#b33640"
    draw.rectangle((0, 0, 1800, 100), fill=ink)
    draw.text((65, 20), "A95 | VINMEC - TÓM TẮT HỒ SƠ XUẤT VIỆN", font=font(38, True), fill="white")
    members = [
        "Chu Quang Linh | Quanglinh1286@gmail.com    •    Nguyễn Minh Quân | minhquandhtb@gmail.com",
        "Trương Thu Hà | thuha261102@gmail.com    •    Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com",
        "Nguyễn Lương Phúc | luongphuc.lpu@gmail.com",
    ]
    for index, line in enumerate(members):
        draw.text((65, 115 + index * 32), line, font=font(23), fill=muted)
    draw.text((65, 230), "MÔ PHỎNG BÀI LAB • Thời gian là giả định, chưa có dữ liệu vận hành thực tế.", font=font(27, True), fill=blue)
    steps = [
        ("01", "Tập hợp đúng hồ sơ", "4 phút", "Bác sĩ / Điều dưỡng • EHR", "Mã người bệnh / đợt điều trị → tập nguồn", False),
        ("02", "Rà diễn biến / xét nghiệm", "5 phút", "Bác sĩ • Ghi chép / Kết quả", "Tập nguồn → diễn biến và kết quả đang chờ", True),
        ("03", "Tổng hợp thuốc / chẩn đoán", "6 phút", "Bác sĩ / Dược sĩ • Đơn xuất viện", "Nguồn → chẩn đoán, thuốc và dị ứng", True),
        ("04", "Viết và đối chiếu tóm tắt", "4 phút", "Bác sĩ • Mẫu tóm tắt xuất viện", "Thông tin đã tổng hợp → bản nháp đối chiếu", False),
        ("05", "Bác sĩ ký và chuyển giao", "1 phút", "Bác sĩ • EHR / Tài liệu bàn giao", "Bản được duyệt → tài liệu chuyển giao", False),
    ]
    handoffs = [
        "Handoff 1: Điều dưỡng → bác sĩ; xác minh đúng người và đợt điều trị",
        "Handoff 2: EHR → bác sĩ; đối chiếu ghi chép và kết quả đang chờ",
        "Handoff 3: Bác sĩ ↔ dược sĩ khi cần làm rõ thông tin thuốc",
        "Handoff 4: Bác sĩ → điều dưỡng / người tiếp nhận sau bước ký",
    ]
    for i, (number, title, duration, actor, data, bottleneck) in enumerate(steps):
        y = 300 + i * 218
        edge = red if bottleneck else "#d3dce8"
        draw.rounded_rectangle((65, y, 1735, y + 158), radius=18, fill="white", outline=edge, width=3)
        draw.rounded_rectangle((85, y + 25, 165, y + 105), radius=15, fill=red if bottleneck else blue)
        draw.text((100, y + 39), number, font=font(36, True), fill="white")
        draw.text((195, y + 20), title, font=font(32, True), fill=ink)
        draw.text((195, y + 76), actor, font=font(25), fill=muted)
        wrap(draw, data, (900, y + 79), 790, font(25), ink, 32)
        draw.text((1480, y + 20), duration, font=font(32, True), fill=red if bottleneck else blue)
        if bottleneck:
            draw.text((900, y + 23), "BOTTLENECK", font=font(24, True), fill=red)
        if i < 4:
            draw.line((125, y + 159, 125, y + 205), fill=blue, width=4)
            draw.polygon([(116, y + 195), (134, y + 195), (125, y + 208)], fill=blue)
            draw.text((195, y + 169), handoffs[i], font=font(24), fill=blue)
    draw.rounded_rectangle((65, 1410, 1735, 1545), radius=18, fill=ink)
    draw.text((90, 1422), "Tổng: 20 phút/hồ sơ  |  Bottleneck: 11 phút ở bước 2 + 3", font=font(30, True), fill="white")
    draw.text((90, 1471), "Số liệu giả định. Không tính thời gian điều trị / chờ xét nghiệm. Bác sĩ chịu trách nhiệm duyệt.", font=font(24), fill="#ced9e7")
    metadata = PngInfo()
    metadata.add_text("Description", __doc__)
    image.save(ROOT / "04-workflow-diagram.png", pnginfo=metadata)


if __name__ == "__main__":
    main()
