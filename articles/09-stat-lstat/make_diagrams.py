from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
W, H = 1440, 810
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


def prepare(name):
    image = Image.open(OUT / name).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")
    return image


def panel(draw, box, fill=(4, 16, 32, 180), outline=(102, 190, 255, 210), radius=12, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size=24, fill=(235, 244, 255, 255), anchor="la"):
    draw.text(xy, value, font=font(size), fill=fill, anchor=anchor)


def watermark(draw):
    text(draw, (W - 30, H - 24), WATERMARK, size=18, fill=(178, 200, 220, 235), anchor="ra")


def kernel_path():
    image = prepare("ai-stat-lstat-kernel-base.png")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 0, W, 62), fill=(4, 15, 29, 225))
    text(draw, (30, 31), "第二章机制：路径查询如何经过用户态、VFS 和 inode", size=25)

    # Layer labels are deliberately short; the adjacent objects carry the detail.
    labels = [
        (78, 112, "用户态：C 调用"),
        (78, 237, "系统调用入口"),
        (78, 349, "VFS：路径解析"),
        (78, 487, "目录项与 inode"),
        (78, 675, "结果回到用户缓冲区"),
    ]
    for x, y, value in labels:
        panel(draw, (x - 14, y - 24, x + 205, y + 14), fill=(4, 16, 32, 205), outline=(93, 180, 240, 170), radius=8, width=1)
        text(draw, (x, y - 4), value, size=19, fill=(208, 232, 250, 255))

    # User call and output buffer.
    panel(draw, (510, 83, 930, 148), fill=(4, 16, 32, 210), outline=(93, 180, 240, 170), radius=8, width=1)
    text(draw, (530, 104), 'stat("link", &st)   /   lstat("link", &st)', size=21, fill=(236, 246, 255, 255))

    # Syscall boundary.
    panel(draw, (470, 224, 970, 278), fill=(4, 16, 32, 190), outline=(93, 180, 240, 160), radius=8, width=1)
    text(draw, (505, 251), "路径名 + 输出地址 → 内核路径状态查询", size=20, fill=(220, 235, 250, 255))

    # VFS and object names.
    text(draw, (470, 367), "按路径组件查找目录项（dentry）", size=20, fill=(215, 242, 225, 255))
    text(draw, (950, 390), "Linux 实现：nameidata → struct path", size=16, fill=(178, 222, 240, 235))
    text(draw, (442, 478), "link", size=18, fill=(255, 214, 120, 255))
    text(draw, (640, 478), "符号链接 inode", size=18, fill=(215, 232, 255, 255))
    text(draw, (1055, 478), "目标 inode", size=18, fill=(215, 232, 255, 255))
    panel(draw, (420, 565, 1060, 640), fill=(4, 16, 32, 225), outline=(100, 180, 235, 140), radius=8, width=1)
    text(draw, (445, 587), "stat：跟随最后一个链接 → 目标 inode", size=17, fill=(125, 238, 167, 255))
    text(draw, (445, 618), "lstat：停在最后一个链接 → 链接 inode", size=17, fill=(120, 211, 255, 255))

    # The lower panels make the returned fields explicit.
    panel(draw, (450, 663, 800, 735), fill=(4, 16, 32, 205), outline=(255, 193, 82, 180), radius=8, width=1)
    text(draw, (470, 686), "lstat：S_IFLNK / 链接文本长度", size=17, fill=(255, 220, 150, 255))
    panel(draw, (930, 663, 1320, 735), fill=(4, 16, 32, 205), outline=(71, 225, 179, 180), radius=8, width=1)
    text(draw, (950, 686), "stat：目标类型 / 大小 / inode", size=17, fill=(166, 255, 210, 255))

    watermark(draw)
    image.convert("RGB").save(OUT / "img-stat-lstat-resolution.png", "PNG")


def inode_relation():
    image = prepare("ai-stat-lstat-inode-base.png")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 0, W, 62), fill=(4, 15, 29, 225))
    text(draw, (30, 31), "目录项、符号链接 inode、目标 inode：三者不是同一个对象", size=25)

    # Upper directory entry panel.
    panel(draw, (472, 66, 954, 183), fill=(4, 16, 32, 185), outline=(90, 190, 255, 190), radius=8, width=1)
    text(draw, (505, 91), "目录项：link", size=21, fill=(222, 242, 255, 255))
    text(draw, (505, 128), "保存文本：stat_lstat_target.tmp", size=17, fill=(205, 230, 250, 255))
    text(draw, (1005, 266), "stat：沿箭头读取目标 inode", size=19, fill=(255, 220, 135, 255))
    text(draw, (495, 266), "lstat：停在链接 inode", size=19, fill=(140, 226, 255, 255))

    # Link inode and target inode fields.
    panel(draw, (162, 275, 430, 449), fill=(4, 16, 32, 185), outline=(56, 220, 255, 200), radius=8, width=1)
    text(draw, (184, 305), "符号链接 inode", size=20, fill=(126, 235, 255, 255))
    text(draw, (184, 345), "类型：S_IFLNK", size=17)
    text(draw, (184, 376), "st_size：21", size=17)
    text(draw, (184, 407), "st_ino：链接自己的编号", size=17)

    panel(draw, (1010, 275, 1284, 449), fill=(4, 16, 32, 185), outline=(255, 207, 85, 200), radius=8, width=1)
    text(draw, (1032, 305), "目标 inode", size=20, fill=(255, 221, 126, 255))
    text(draw, (1032, 345), "类型：S_IFREG", size=17)
    text(draw, (1032, 376), "st_size：目标大小", size=17)
    text(draw, (1032, 407), "st_ino：目标编号", size=17)

    # Dangling case.
    panel(draw, (160, 585, 444, 753), fill=(4, 16, 32, 190), outline=(64, 170, 230, 170), radius=8, width=1)
    text(draw, (182, 616), "链接 inode 仍存在", size=19, fill=(140, 226, 255, 255))
    text(draw, (182, 652), "lstat(link) → 成功", size=17, fill=(152, 245, 188, 255))
    text(draw, (182, 686), "st_size 仍是 21", size=17, fill=(205, 230, 250, 255))

    panel(draw, (1005, 585, 1288, 753), fill=(32, 8, 16, 190), outline=(255, 90, 102, 200), radius=8, width=1)
    text(draw, (1027, 616), "目标目录项已删除", size=19, fill=(255, 151, 158, 255))
    text(draw, (1027, 652), "stat(link) → ENOENT", size=17, fill=(255, 151, 158, 255))
    text(draw, (1027, 686), "目标找不到，不等于链接不存在", size=16, fill=(255, 205, 205, 255))

    watermark(draw)
    image.convert("RGB").save(OUT / "img-stat-lstat-dangling.png", "PNG")


if __name__ == "__main__":
    kernel_path()
    inode_relation()
