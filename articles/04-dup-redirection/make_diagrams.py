from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/PingFang.ttc"
try:
    regular = ImageFont.truetype(FONT, 34)
    small = ImageFont.truetype(FONT, 27)
    title = ImageFont.truetype(FONT, 44)
except OSError:
    regular = ImageFont.load_default()
    small = regular
    title = regular

BG = (248, 250, 252)
INK = (26, 35, 48)
BLUE = (220, 235, 250)
GREEN = (222, 244, 231)
ORANGE = (255, 235, 204)
RED = (244, 220, 220)

def box(draw, xy, text, fill, font=regular):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=INK, width=3)
    lines = text.split("\n")
    heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total = sum(heights) + (len(lines) - 1) * 8
    y = (y1 + y2 - total) / 2
    for line, h in zip(lines, heights):
        w = draw.textbbox((0, 0), line, font=font)[2]
        draw.text(((x1 + x2 - w) / 2, y), line, fill=INK, font=font)
        y += h + 8

def arrow(draw, a, b, label=None):
    draw.line([a, b], fill=INK, width=5)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - 18 * math.cos(ang - 0.5), b[1] - 18 * math.sin(ang - 0.5))
    p2 = (b[0] - 18 * math.cos(ang + 0.5), b[1] - 18 * math.sin(ang + 0.5))
    draw.polygon([b, p1, p2], fill=INK)
    if label:
        draw.text(((a[0] + b[0]) / 2 + 8, (a[1] + b[1]) / 2 - 42), label, fill=INK, font=small)

def shared():
    im = Image.new("RGB", (1600, 900), BG)
    d = ImageDraw.Draw(im)
    d.text((55, 35), "dup 复制的是描述符表项，不是 struct file", fill=INK, font=title)
    box(d, (70, 170, 430, 720), "进程\n文件描述符表", BLUE)
    box(d, (540, 220, 900, 400), "fd 3\n指针", GREEN)
    box(d, (540, 500, 900, 680), "fd 4\n指针", GREEN)
    box(d, (1080, 300, 1510, 600), "同一个 struct file\n\nf_pos = 2\nf_flags\nf_inode → inode", ORANGE)
    arrow(d, (430, 300), (540, 310), "dup")
    arrow(d, (430, 590), (540, 590), "dup")
    arrow(d, (900, 310), (1080, 420))
    arrow(d, (900, 590), (1080, 480))
    d.text((80, 790), "两个 fd 关闭顺序可以不同，但偏移量和文件状态标志由同一个打开文件对象共享。", fill=INK, font=small)
    im.save("img-shared-file-object.png")

def redirect():
    im = Image.new("RGB", (1600, 900), BG)
    d = ImageDraw.Draw(im)
    d.text((55, 35), "dup2(oldfd, STDOUT_FILENO) 的重定向路径", fill=INK, font=title)
    box(d, (60, 170, 410, 700), "程序\nwrite(1, ...)\ndprintf(1, ...)", BLUE)
    box(d, (550, 190, 910, 360), "进程 fd 表\n1 → 终端", GREEN)
    box(d, (550, 510, 910, 680), "进程 fd 表\n1 → 输出文件", GREEN)
    box(d, (1080, 220, 1510, 370), "终端\n(原来的目标)", ORANGE)
    box(d, (1080, 530, 1510, 680), "dup_demo_stdout.txt\n(新的目标)", ORANGE)
    arrow(d, (410, 300), (550, 275), "调用前")
    arrow(d, (910, 275), (1080, 295))
    arrow(d, (410, 580), (550, 595), "dup2 后")
    arrow(d, (910, 595), (1080, 605))
    d.text((80, 790), "dup2 会原子地让 newfd 指向 oldfd 的同一打开文件对象；恢复 stdout 只需再次 dup2 保存的副本。", fill=INK, font=small)
    im.save("img-dup2-redirection.png")

if __name__ == "__main__":
    shared()
    redirect()
