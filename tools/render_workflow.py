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
    draw.text((65, 20), "A95 | XANH SM - QUY TRÌNH HIỆN TẠI", font=font(38, True), fill="white")
    members = [
        "Chu Quang Linh | Quanglinh1286@gmail.com    •    Nguyễn Minh Quân | minhquandhtb@gmail.com",
        "Trương Thu Hà | thuha261102@gmail.com    •    Phan Trần Mạnh Cường | manhcuong2005.28@gmail.com",
        "Nguyễn Lương Phúc | luongphuc.lpu@gmail.com",
    ]
    for index, line in enumerate(members):
        draw.text((65, 115 + index * 32), line, font=font(23), fill=muted)
    draw.text((65, 230), "MÔ PHỎNG BÀI LAB • Thời gian là giả định, chưa có dữ liệu vận hành thực tế.", font=font(27, True), fill=blue)
    steps = [
        ("01", "Nhận báo cáo sự cố", "2 phút", "Điều phối viên • Điện thoại / App", "Báo cáo tài xế → ticket sự cố", False),
        ("02", "Xác minh pin và GPS", "2 phút", "Điều phối viên • Dashboard xe", "Ticket → pin / vị trí đã kiểm tra", False),
        ("03", "Tra phương án sạc", "5 phút", "Điều phối viên • Dashboard trạm", "Pin / GPS → trạm phù hợp hoặc cứu hộ", True),
        ("04", "Soạn và duyệt tin", "5 phút", "Điều phối viên • Mẫu tin / App", "Phương án → bản hướng dẫn đã duyệt", True),
        ("05", "Gửi hoặc liên hệ cứu hộ", "1 phút", "Điều phối viên • App / Điện thoại", "Bản duyệt → yêu cầu được bàn giao", False),
    ]
    handoffs = [
        "Handoff 1: Tài xế → điều phối viên khi báo sự cố",
        "Handoff 2: Điều phối viên ↔ hệ thống xe để xác minh",
        "Handoff 3: Điều phối viên ↔ dữ liệu trạm để chọn phương án",
        "Handoff 4: Điều phối viên → tài xế / đội cứu hộ ở bước gửi",
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
    draw.text((90, 1422), "Tổng: 15 phút/lượt  |  Bottleneck: 10 phút ở bước 3 + 4", font=font(30, True), fill="white")
    draw.text((90, 1471), "Pin nguy cấp ưu tiên cứu hộ. Không tính thời gian chờ xe cứu hộ hoặc thời gian sạc.", font=font(24), fill="#ced9e7")
    metadata = PngInfo()
    metadata.add_text("Description", __doc__)
    image.save(ROOT / "04-workflow-diagram.png", pnginfo=metadata)


if __name__ == "__main__":
    main()
