from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
WATERMARK = "公众号·理解力笔记"


def font(size):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def base(size):
    image = Image.new("RGB", size, "#101820")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, size[0], 70), fill="#1f2a35")
    draw.ellipse((28, 25, 46, 43), fill="#ff5f57")
    draw.ellipse((58, 25, 76, 43), fill="#febc2e")
    draw.ellipse((88, 25, 106, 43), fill="#28c840")
    return image, draw


def rounded(draw, box, fill, outline="#4c6375", radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def watermark(draw, size):
    f = font(22)
    text = WATERMARK
    bbox = draw.textbbox((0, 0), text, font=f)
    draw.text((size[0] - (bbox[2] - bbox[0]) - 28, size[1] - 42), text, font=f, fill="#9fb3c4")


def diagram_lookup():
    size = (1400, 760)
    image, draw = base(size)
    title = font(30)
    body = font(26)
    small = font(22)
    draw.text((135, 22), "stat：路径如何变成元数据快照", font=title, fill="#e6edf3")

    rounded(draw, (70, 180, 330, 510), "#162633", "#33b5e5")
    draw.text((105, 215), "用户态", font=body, fill="#65d6ff")
    rounded(draw, (100, 285, 300, 390), "#0d1117", "#5f7f95")
    draw.text((130, 315), "stat(path,", font=body, fill="#f0f6fc")
    draw.text((130, 350), "&st)", font=body, fill="#f0f6fc")
    draw.text((112, 435), "path 是名字，st 是接收结果的缓冲区", font=small, fill="#b7c7d4")

    rounded(draw, (460, 180, 760, 510), "#1a2933", "#e4a64f")
    draw.text((510, 215), "内核路径解析", font=body, fill="#ffc66d")
    rounded(draw, (500, 285, 720, 390), "#0d1117", "#5f7f95")
    draw.text((522, 315), "目录项 → inode", font=body, fill="#f0f6fc")
    draw.text((505, 435), "目录项负责把名字映射到对象", font=small, fill="#b7c7d4")

    rounded(draw, (890, 180, 1330, 510), "#1b2a22", "#56d364")
    draw.text((960, 215), "返回 struct stat", font=body, fill="#8be28f")
    fields = ["st_mode   类型 + 权限", "st_size   字节数", "st_ino    inode 编号", "st_mtime  内容修改时间"]
    for i, line in enumerate(fields):
        draw.text((935, 285 + i * 48), line, font=small, fill="#e6edf3")

    draw.line((330, 345, 460, 345), fill="#65d6ff", width=5)
    draw.polygon([(460, 345), (438, 332), (438, 358)], fill="#65d6ff")
    draw.line((760, 345, 890, 345), fill="#ffc66d", width=5)
    draw.polygon([(890, 345), (868, 332), (868, 358)], fill="#ffc66d")
    draw.text((77, 580), "一次 stat 只是查询时刻的快照，不能替代后续操作的错误处理。", font=body, fill="#ffcf70")
    watermark(draw, size)
    image.save(OUT / "img-stat-lookup.png")


def diagram_fields():
    size = (1280, 720)
    image, draw = base(size)
    title = font(30)
    body = font(25)
    small = font(21)
    draw.text((135, 22), "struct stat：字段各自回答什么问题", font=title, fill="#e6edf3")

    rounded(draw, (70, 150, 520, 620), "#162633", "#33b5e5")
    draw.text((110, 180), "身份与类型", font=body, fill="#65d6ff")
    left = [
        ("st_dev + st_ino", "对象在哪个文件系统，inode 编号是多少"),
        ("st_mode", "类型宏 + 权限位"),
        ("st_nlink", "有多少个硬链接"),
        ("st_uid / st_gid", "属主与属组"),
    ]
    for i, (a, b) in enumerate(left):
        y = 250 + i * 78
        draw.text((105, y), a, font=body, fill="#f0f6fc")
        draw.text((105, y + 34), b, font=small, fill="#b7c7d4")

    rounded(draw, (650, 150, 1210, 620), "#1b2a22", "#56d364")
    draw.text((690, 180), "大小与时间", font=body, fill="#8be28f")
    right = [
        ("st_size", "普通文件的字节数，目录值不要当条目数"),
        ("st_atime", "最近访问时间，可能受挂载选项影响"),
        ("st_mtime", "内容最近一次修改时间"),
        ("st_ctime", "Linux 上的 inode 状态改变时间"),
    ]
    for i, (a, b) in enumerate(right):
        y = 250 + i * 78
        draw.text((685, y), a, font=body, fill="#f0f6fc")
        draw.text((685, y + 34), b, font=small, fill="#b7c7d4")
    watermark(draw, size)
    image.save(OUT / "img-stat-fields.png")


if __name__ == "__main__":
    diagram_lookup()
    diagram_fields()
