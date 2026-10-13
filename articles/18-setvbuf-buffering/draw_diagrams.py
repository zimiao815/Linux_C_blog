from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ART=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/PingFang.ttc'
INK,BLUE,TEAL,GRAY='#18334d','#2267ad','#087f8c','#576a7a'
def canvas(h):
    im=Image.new('RGB',(1200,h),'white'); return im,ImageDraw.Draw(im)
def text(d,xy,value,size=27,color=INK):
    d.multiline_text(xy,value,font=ImageFont.truetype(FONT,size),fill=color,spacing=12)
def box(d,rect,title,detail='',color=BLUE):
    d.rounded_rectangle(rect,radius=18,fill='#f2f7fb',outline=color,width=3)
    x,y,_,_=rect; text(d,(x+22,y+18),title,30,color)
    if detail: text(d,(x+22,y+68),detail,25)
def arrow(d,start,end,color=BLUE):
    x,y=start; a,b=end; d.line((start,end),fill=color,width=4)
    angle=math.atan2(b-y,a-x)
    d.polygon([(a,b),(a-15*math.cos(angle-.45),b-15*math.sin(angle-.45)),(a-15*math.cos(angle+.45),b-15*math.sin(angle+.45))],fill=color)
def watermark(d,h): text(d,(890,h-49),'公众号·理解力笔记',23,GRAY)

im,d=canvas(1200)
text(d,(48,28),'setvbuf 配置的是流的用户态缓冲',39)
text(d,(48,92),'普通文件输出示意：glibc 2.40 / Linux v6.6；非实测内存快照',25,TEAL)
box(d,(55,153,490,432),'stdout → FILE','_flags：缓冲模式\n_IO_buf_base / _IO_buf_end\n_IO_write_base / _IO_write_ptr\n_fileno = 1')
box(d,(745,178,1145,397),'调用方自备数组','static char buffer[4096]\n库借用这块存储\n数组保持有效到流关闭',TEAL)
arrow(d,(492,278),(743,278),TEAL); text(d,(528,231),'缓冲区指针',25,TEAL)
text(d,(65,458),'setvbuf 改模式与缓冲关联；后续 I/O 根据策略提交数据。',27)
d.line((40,528,1160,528),fill='#a5b5c3',width=2)
text(d,(48,548),'内核态：提交时，write 等底层操作使用 fd 查表',27,TEAL)
box(d,(48,623,342,778),'files_struct','fdt')
box(d,(442,623,764,778),'fdtable','fd[1]：struct file *')
arrow(d,(344,705),(440,705))
box(d,(442,865,764,1067),'struct file','f_pos：文件偏移\nf_inode：inode 指针\nf_op：文件操作')
arrow(d,(604,780),(604,863))
box(d,(891,891,1153,1042),'inode','文件的元数据')
arrow(d,(766,961),(889,961))
text(d,(48,1105),'改变用户态缓冲，不会把文件或管道变成终端，也不保证落盘。',26,GRAY)
watermark(d,1200); im.save(ART/'img-setvbuf-objects.png')

im,d=canvas(960)
text(d,(48,28),'自备缓冲区，要活得比流的使用期更久',39)
text(d,(48,94),'这里画的是动态分配缓冲区；同一数组不要同时交给多个流。',25,GRAY)
box(d,(240,158,960,272),'打开流，分配数组','在流上做其他操作前准备好缓冲区')
arrow(d,(600,274),(600,325))
box(d,(240,328,960,442),'setvbuf 成功，库开始借用数组','调用方保留所有权；期间不读写、不释放数组',TEAL)
arrow(d,(600,444),(600,497),TEAL)
box(d,(240,500,960,614),'执行流 I/O','把数组留给标准 I/O 库管理内部状态',TEAL)
arrow(d,(600,616),(600,669),TEAL)
box(d,(240,672,960,786),'fclose 返回后，再 free 数组','检查关闭结果；关闭失败也不能再次 fclose')
d.line((147,349,147,772),fill=TEAL,width=6)
text(d,(47,453),'数组\n必须\n有效',27,TEAL)
text(d,(75,833),'局部数组也能用：必须在离开它所在作用域之前关闭流。',27)
watermark(d,960); im.save(ART/'img-buffer-lifetime.png')
print('saved two diagrams')
