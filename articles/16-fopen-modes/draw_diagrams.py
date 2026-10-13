from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ART = Path(__file__).resolve().parent
FONT = '/System/Library/Fonts/PingFang.ttc'
INK, BLUE, TEAL, GRAY = '#18334d', '#2267ad', '#087f8c', '#576a7a'

def canvas(h):
    im = Image.new('RGB', (1200, h), 'white')
    return im, ImageDraw.Draw(im)

def text(d, xy, value, size=27, color=INK):
    d.multiline_text(xy, value, font=ImageFont.truetype(FONT,size), fill=color, spacing=12)

def box(d, rect, title, detail='', color=BLUE):
    d.rounded_rectangle(rect, radius=18, fill='#f2f7fb', outline=color, width=3)
    x,y,_,_=rect
    text(d,(x+22,y+18),title,30,color)
    if detail: text(d,(x+22,y+68),detail,25)

def arrow(d, start, end, color=BLUE, dashed=False):
    x,y=start; a,b=end
    if dashed:
        length=math.hypot(a-x,b-y)
        for t in range(0,int(length),18):
            p=t/length; q=min(t+10,length)/length
            d.line((x+(a-x)*p,y+(b-y)*p,x+(a-x)*q,y+(b-y)*q),fill=color,width=4)
    else: d.line((start,end),fill=color,width=4)
    angle=math.atan2(b-y,a-x)
    pts=[(a,b),(a-15*math.cos(angle-.45),b-15*math.sin(angle-.45)),(a-15*math.cos(angle+.45),b-15*math.sin(angle+.45))]
    d.polygon(pts,fill=color)

def watermark(d,h): text(d,(890,h-49),'公众号·理解力笔记',23,GRAY)

im,d=canvas(1150)
text(d,(48,28),'w+：截断发生在打开阶段',40)
text(d,(48,93),'用户态 · glibc 2.40 的普通文件流',25,TEAL)
box(d,(80,145,1120,266),'fopen(path, "w+")','库解析模式；成功后返回 FILE *，关联底层 fd')
arrow(d,(600,268),(600,320))
box(d,(80,323,1120,436),'交给底层打开操作的标志','O_RDWR  |  O_CREAT  |  O_TRUNC')
d.line((40,477,1160,477),fill='#a5b5c3',width=2)
text(d,(48,495),'内核态 · Linux v6.6',25,TEAL)
arrow(d,(600,438),(600,546))
box(d,(80,548,1120,672),'已有普通文件：处理截断','handle_truncate → do_truncate(length = 0)','#b87716')
text(d,(48,722),'打开成功后，描述符关联的对象',29)
box(d,(38,813,298,1009),'files_struct','fdt')
box(d,(367,813,585,1009),'fdtable','fd[3]')
box(d,(655,813,887,1009),'struct file','f_pos\nf_inode')
box(d,(957,813,1170,1009),'inode','i_size = 0','#b87716')
arrow(d,(300,905),(365,905))
arrow(d,(587,905),(653,905))
arrow(d,(889,955),(955,955))
arrow(d,(1060,674),(1060,811),'#b87716')
text(d,(900,748),'截断后的长度',22,'#a55d12')
text(d,(48,1055),'此时应用还没有写入正文；fclose 不会恢复原来的内容。',27,GRAY)
watermark(d,1150)
im.save(ART/'img-wplus-truncation.png')

im,d=canvas(980)
text(d,(48,28),'先决定怎么处理原文件，再选模式',39)
text(d,(48,92),'仅针对普通文件；打开是否成功仍受权限和路径条件限制。',25,GRAY)
rows=[('只读取内容','r','必须已存在'),('修改已有位置','r+','不截断；写入会覆盖对应字节'),('把新内容接到末尾','a / a+','不存在则创建；写入始终追加'),('允许丢弃原内容、重新生成','w / w+','已有文件会在打开时清空'),('只允许创建一个新文件','wx','已有同名文件就失败')]
for i,(need,mode,note) in enumerate(rows):
 y=153+i*135
 d.rounded_rectangle((48,y,1152,y+115),radius=15,fill='#f2f7fb',outline='#d4e2ed',width=2)
 text(d,(75,y+15),need,29)
 text(d,(75,y+60),note,24,GRAY)
 text(d,(900,y+34),mode,35,TEAL if i!=3 else '#b87716')
d.rounded_rectangle((48,854,1152,916),radius=12,fill='#fff3e5')
text(d,(72,867),'“+” 增加读写能力，不改变首字母规定的截断或追加行为。',27,'#8b5012')
watermark(d,980)
im.save(ART/'img-mode-choice.png')
print('saved two diagrams')
