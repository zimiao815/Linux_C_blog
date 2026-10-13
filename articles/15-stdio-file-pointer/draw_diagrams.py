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

im,d=canvas(1170)
text(d,(48,26),'FILE *、fd 与内核对象，各在一层',40)
text(d,(48,88),'用户态  ·  glibc 2.40 的普通文件流',25,TEAL)
box(d,(48,166,210,272),'fp','FILE *')
arrow(d,(212,217),(280,217))
box(d,(282,142,748,367),'FILE 流对象（节选）','_flags：EOF / 错误标志\n_fileno = 3\n_IO_read_ptr / _IO_read_end')
box(d,(856,165,1150,360),'用户态缓冲区','暂存读取的字节\n字段记录边界\n及当前读取位置',TEAL)
arrow(d,(750,325),(854,325),TEAL)
text(d,(777,282),'指针',23,TEAL)
d.line((40,420,1160,420),fill='#a5b5c3',width=2)
text(d,(48,441),'内核态  ·  Linux v6.6',25,TEAL)
box(d,(48,555,335,704),'files_struct','fdt')
arrow(d,(336,644),(430,644))
text(d,(344,597),'指针',23)
box(d,(432,544,804,731),'fdtable','fd：描述符指针数组\nfd[3] → struct file')
arrow(d,(611,369),(611,540),'#be6d16',True)
# Keep the numeric lookup explanation outside the objects.
d.rectangle((625,376,1170,412), fill='white')
text(d,(630,377),'虚线：整数 fd 用于查表',24,'#a55d12')
text(d,(846,567),'fd = 3 是索引，\n不是跨越边界\n的内存指针。',25,GRAY)
box(d,(432,847,804,1050),'struct file','f_pos：内核文件偏移\nf_inode：inode 指针')
arrow(d,(617,733),(617,844))
text(d,(638,773),'槽位保存指针',24)
box(d,(912,873,1152,1022),'inode','文件系统对象')
arrow(d,(806,971),(909,971))
text(d,(48,1080),'示意仅保留本文需要的字段；FILE 的字段不是应用程序接口。',25,GRAY)
watermark(d,1170)
im.save(ART/'img-stream-objects.png')

im,d=canvas(820)
text(d,(48,30),'fileno 取出编号，fclose 负责收尾',40)
box(d,(70,116,410,287),'fopen 成功','返回 FILE *\n流关联底层 fd')
arrow(d,(412,200),(573,200))
box(d,(575,116,1125,287),'fileno(fp)','返回现有 fd 的整数值\n没有复制 fd，也没有转移关闭责任')
arrow(d,(240,289),(240,391))
box(d,(70,394,575,573),'fclose(fp)','处理流的缓冲与资源\n并关闭所关联的 fd')
arrow(d,(577,479),(705,479))
box(d,(707,394,1125,573),'检查返回值','成功为 0，失败为 EOF\n两种结果都不可再用 fp',TEAL)
d.rounded_rectangle((70,625,1125,725),radius=15,fill='#fff3e5',outline='#c88225',width=2)
text(d,(96,644),'不要先 close(fileno(fp))，再对这个流调用 fclose。\n也不要重试 fclose，或对同一个 FILE * 调用 free。',26,'#8b5012')
watermark(d,820)
im.save(ART/'img-stream-lifetime.png')
print('saved two diagrams')
