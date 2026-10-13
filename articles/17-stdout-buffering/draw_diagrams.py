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

im,d=canvas(930)
text(d,(48,28),'同一行输出，暂停时停在不同地方',39)
text(d,(48,92),'实验条件：默认缓冲，小量输出，尚未显式刷新 stdout。',25,GRAY)
box(d,(70,151,1130,265),'printf("ready\\n")','调用成功后，程序进入等待；此时检查接收端。')
arrow(d,(340,267),(340,335))
arrow(d,(860,267),(860,335))
box(d,(70,338,575,535),'stdout 接终端：行缓冲','换行触发提交\n接收端已经读到 ready\\n',TEAL)
box(d,(625,338,1130,535),'stdout 接文件或管道：全缓冲','小量数据仍在用户态缓冲中\n接收端暂未读到字节','#b87716')
arrow(d,(340,537),(340,605),TEAL)
arrow(d,(860,537),(860,605),'#b87716',True)
box(d,(70,608,575,737),'终端','ready 已可见',TEAL)
box(d,(625,608,1130,737),'文件 / 管道','暂无输出；不代表 printf 没执行','#b87716')
d.rounded_rectangle((70,783,1130,852),radius=15,fill='#f2f7fb')
text(d,(94,802),'加上成功的 fflush(stdout)：三种目标在暂停前都收到 ready\\n。',26)
watermark(d,930)
im.save(ART/'img-buffer-comparison.png')

im,d=canvas(1220)
text(d,(48,28),'缓冲在用户态，描述符表关联内核对象',39)
text(d,(48,92),'示意：stdout 被重定向到普通文件；glibc 2.40 / Linux v6.6',25,TEAL)
box(d,(65,147,455,387),'stdout → FILE','_fileno = 1\n_flags：缓冲策略\n_IO_write_base\n_IO_write_ptr')
box(d,(690,147,1135,387),'用户态输出缓冲','ready\\n 暂存在这里\n\n尚未交给内核',TEAL)
arrow(d,(457,277),(688,277),TEAL)
text(d,(494,234),'缓冲区指针',23,TEAL)
text(d,(65,405),'库决定提交时，通过 fd = 1 发起底层写入。',28)
d.line((40,466,1160,466),fill='#a5b5c3',width=2)
text(d,(48,486),'内核态',27,TEAL)
box(d,(48,581,336,757),'files_struct','fdt')
box(d,(431,581,745,757),'fdtable','fd[1]：struct file *')
arrow(d,(338,678),(429,678))

# Integer lookup is a separate relation from buffer pointers.
text(d,(290,510),'fd = 1 用于查表，不是内核内存指针',24,GRAY)
box(d,(431,850,745,1070),'struct file','f_pos：文件偏移\nf_inode：inode 指针\nf_op：文件操作')
arrow(d,(588,759),(588,848))
box(d,(873,878,1149,1045),'inode','关联的文件对象')
arrow(d,(747,958),(871,958))
text(d,(48,1110),'文件内容可读，不等于断电后仍可靠保存；本图不表示持久化。',26,GRAY)
watermark(d,1220)
im.save(ART/'img-stdout-objects.png')
print('saved two diagrams')
