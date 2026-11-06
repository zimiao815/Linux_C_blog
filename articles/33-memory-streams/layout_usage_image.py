"""Reflow AI-generated boxes into readable columns; preserve generated labels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
from collections import deque
p = Path(__file__).resolve().parent
src = p / 'memory-usage-ai-original.png'
if not src.exists():
    Image.open(p / 'memory-usage.png').save(src)
im = Image.open(src).convert('RGB').resize((2048, 683), Image.Resampling.LANCZOS)
out = Image.new('RGB', (1080, 1410), 'white')
draw = ImageDraw.Draw(out)
def put(box, x, y, w=470, h=130, frame=False):
    crop = im.crop(box)
    if frame:
        pixels = crop.load()
        points = {(a,b) for a in range(crop.width) for b in range(crop.height)
                  if pixels[a,b][2] > pixels[a,b][0] + 30 and pixels[a,b][2] > pixels[a,b][1] + 20}
        boxes = []
        while points:
            start = points.pop()
            q = deque([start])
            xs, ys = [start[0]], [start[1]]
            while q:
                a,b = q.popleft()
                for point in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                    if point in points:
                        points.remove(point)
                        q.append(point)
                        xs.append(point[0]); ys.append(point[1])
            boxes.append((min(xs),min(ys),max(xs)+1,max(ys)+1))
        a,b,c,d = max(boxes,key=lambda v:(v[2]-v[0])*(v[3]-v[1]))
        crop = crop.crop((max(0,a-2),max(0,b-2),min(crop.width,c+2),min(crop.height,d+2)))
    crop = ImageOps.contain(crop, (w, h), Image.Resampling.LANCZOS)
    out.paste(crop, (x + (w-crop.width)//2, y + (h-crop.height)//2))
def arrow(x, y):
    draw.line([(x,y),(x,y+40)], fill='#0017b8', width=5)
    draw.polygon([(x-11,y+28),(x+11,y+28),(x,y+43)], fill='#0017b8')
put((400,0,1490,130),30,10,1020,130)
put((15,170,428,295),30,175,frame=True)
put((0,350,449,476),580,175,frame=True)
left=[(489,170,831,295),(889,170,1234,295),(1263,170,1609,295),(1619,170,1948,295)]
right=[(503,352,800,474),(830,352,1119,474),(1168,352,1447,474),(1479,347,1742,480),(1787,350,2048,476)]
for x, boxes in [(30,left),(580,right)]:
    for i,box in enumerate(boxes):
        y=350+i*185
        put(box,x,y,frame=True)
        if i+1 < len(boxes): arrow(x+235,y+135)
# The function names above each column are labels, not a step before allocation.
put((1610,595,2044,665),600,1320,440,70)
out.save(p / 'memory-usage.png')
print(out.size)
