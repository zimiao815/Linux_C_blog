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

def arrow(draw, a, b, label=None, color=INK):
    draw.line([a, b], fill=color, width=5)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - 18 * math.cos(ang - 0.5), b[1] - 18 * math.sin(ang - 0.5))
    p2 = (b[0] - 18 * math.cos(ang + 0.5), b[1] - 18 * math.sin(ang + 0.5))
    draw.polygon([b, p1, p2], fill=color)
    if label:
        draw.text(((a[0] + b[0]) / 2 - 10, (a[1] + b[1]) / 2 - 42), label, fill=color, font=small)

def pipeline():
    im = Image.new("RGB", (1600, 900), BG)
    d = ImageDraw.Draw(im)
    d.text((55, 35), "write 成功与稳定存储之间还有几层", fill=INK, font=title)
    box(d, (45, 220, 350, 620), "应用进程\n用户缓冲区\nwrite()", BLUE)
    box(d, (440, 220, 750, 620), "内核\n页缓存\n脏页", GREEN)
    box(d, (840, 220, 1145, 620), "文件系统\n回写队列\n元数据", ORANGE)
    box(d, (1230, 220, 1555, 620), "设备缓存\n稳定存储\n断电后仍可读", RED)
    arrow(d, (350, 420), (440, 420), "write 返回")
    arrow(d, (750, 420), (840, 420), "异步回写")
    arrow(d, (1145, 420), (1230, 420), "设备提交")
    d.rounded_rectangle((805, 150, 1180, 205), radius=14, fill=(255, 246, 180), outline=INK, width=3)
    d.text((835, 162), "fsync(fd)：请求走完关键路径", fill=INK, font=small)
    d.text((70, 760), "write 的成功返回值只说明内核接收了数据；持久化语义要看 fsync/fdatasync 以及硬件保证。", fill=INK, font=small)
    im.save("img-write-durability-pipeline.png")

def scope():
    im = Image.new("RGB", (1600, 900), BG)
    d = ImageDraw.Draw(im)
    d.text((55, 35), "fsync、fdatasync、sync 的作用范围不同", fill=INK, font=title)
    box(d, (80, 180, 440, 680), "fsync(fd)\n\n指定文件的数据\n+ 必要元数据\n\n返回成功后再继续", BLUE)
    box(d, (600, 180, 960, 680), "fdatasync(fd)\n\n指定文件的数据\n+ 恢复数据所需元数据\n\n减少无关元数据等待", GREEN)
    box(d, (1120, 180, 1480, 680), "sync()\n\n系统范围请求回写\n\n不告诉你某个文件\n何时完成持久化", ORANGE)
    d.text((95, 760), "关键文件：逐个 fsync/fdatasync；批量后台回写：sync 只适合作为全局请求，不能替代逐文件确认。", fill=INK, font=small)
    im.save("img-sync-scope.png")

if __name__ == "__main__":
    pipeline()
    scope()
