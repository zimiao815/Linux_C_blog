"""Deterministic fallback after three image-service 504 responses."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

art = Path(__file__).resolve().parent
image = Image.new("RGB", (1500, 1120), "#f9f8f3")
draw = ImageDraw.Draw(image)
font_path = "/System/Library/Fonts/PingFang.ttc"
ink = "#19324c"
blue = "#246aa8"
orange = "#b86216"
red = "#ae4848"

def text(x, y, value, size=36, fill=ink):
    font = ImageFont.truetype(font_path, size)
    draw.text((x, y), value, font=font, fill=fill, anchor="mm")

def box(bounds, fill, outline=None):
    draw.rounded_rectangle(bounds, radius=22, fill=fill, outline=outline, width=3)

def arrow(points, fill=ink):
    draw.line(points, fill=fill, width=5, joint="curve")
    x, y = points[-1]
    a, b = points[-2]
    angle = math.atan2(y-b, x-a)
    tip = [(x, y)]
    for delta in [-0.5, 0.5]:
        tip.append((x-20*math.cos(angle+delta), y-20*math.sin(angle+delta)))
    draw.polygon(tip, fill=fill)

text(750, 60, "fork 之后，从调用返回处继续", 52)
box((510, 120, 990, 230), "#e8edf1")
text(750, 153, "原进程", 32)
text(750, 199, "pid = fork();", 42)

# 两块区域代表互斥结果；成功区域内部才产生两条执行路径。
arrow([(750, 230), (750, 275), (510, 275), (510, 325)])
arrow([(750, 275), (1240, 275), (1240, 325)])
box((40, 325, 1000, 940), "#edf3f8")
box((1040, 325, 1460, 940), "#f8eded")
text(520, 375, "创建成功：父子两条路径", 40)
text(1250, 375, "创建失败", 40, red)

arrow([(520, 420), (520, 460), (280, 460), (280, 510)], blue)
arrow([(520, 460), (760, 460), (760, 510)], orange)
box((80, 510, 480, 675), "#dcebf7", blue)
box((560, 510, 960, 675), "#fff0dc", orange)
text(280, 558, "父进程", 42, blue)
text(280, 622, "pid = 子进程 PID", 34)
text(760, 558, "子进程", 42, orange)
text(760, 622, "pid = 0", 38)

for center, color in [(280, blue), (760, orange)]:
    arrow([(center, 675), (center, 760)], color)
    box((center-200, 760, center+200, 865), "#ffffff")
    text(center, 812, "继续执行后续代码", 34)

arrow([(1250, 420), (1250, 510)], red)
box((1080, 510, 1420, 710), "#ffe2e2", red)
text(1250, 550, "原进程", 40, red)
text(1250, 610, "pid = -1", 38)
text(1250, 668, "没有子进程", 34)
arrow([(1250, 710), (1250, 760)], red)
box((1080, 760, 1420, 865), "#ffffff")
text(1250, 812, "处理错误", 36)

text(750, 1005, "父子谁先运行，没有保证", 42)
text(1260, 1080, "公众号·理解力笔记", 29, "#647586")
image.save(art / "img-fork-branches.png")
preview = image.copy()
preview.thumbnail((677, 1000))
preview.save(art / "images" / "branches-mobile-preview.png")
print("written img-fork-branches.png; 1500x1120")
