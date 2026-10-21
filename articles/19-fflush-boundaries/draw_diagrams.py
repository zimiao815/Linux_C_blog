from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ART=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/PingFang.ttc'
INK,BLUE,TEAL,GRAY='#18334d','#2267ad','#087f8c','#576a7a'
def canvas(h):
    im=Image.new('RGB',(1200,h),'white'); return im,ImageDraw.Draw(im)
def text(d,xy,value,size=27,color=INK):
    d.multiline_text(xy,value,font=ImageFont.truetype(FONT,size),fill=color,spacing=10)
def box(d,rect,title,detail='',color=BLUE):
    d.rounded_rectangle(rect,radius=18,fill='#f2f7fb',outline=color,width=3)
    x,y,_,_=rect; text(d,(x+20,y+16),title,29,color)
    if detail: text(d,(x+20,y+63),detail,25)
def arrow(d,start,end,color=BLUE):
    x,y=start; a,b=end; d.line((start,end),fill=color,width=4)
    angle=math.atan2(b-y,a-x)
    d.polygon([(a,b),(a-15*math.cos(angle-.45),b-15*math.sin(angle-.45)),(a-15*math.cos(angle+.45),b-15*math.sin(angle+.45))],fill=color)
def watermark(d,h): text(d,(890,h-49),'公众号·理解力笔记',23,GRAY)

im,d=canvas(1310)
text(d,(45,25),'fflush 把待输出字节交给底层文件',39)
text(d,(45,88),'普通文件缓冲写路径：glibc 2.40 / Linux v6.6 源码示意',25,TEAL)
text(d,(45,133),'用户态',27,GRAY)
box(d,(45,182,495,414),'stdout → FILE','_IO_write_base\n_IO_write_ptr\n_fileno = 1')
box(d,(745,198,1155,400),'用户态缓冲数组','[base, ptr) 是待输出字节\n刷新成功后不再待输出',TEAL)
arrow(d,(497,284),(743,284),TEAL);text(d,(531,238),'指针指向数组',24,TEAL)
box(d,(45,455,359,554),'_IO_fflush')
box(d,(437,455,797,554),'_IO_new_file_sync')
box(d,(879,455,1155,554),'write(fd, …)')
arrow(d,(361,505),(435,505));arrow(d,(799,505),(877,505))
text(d,(46,575),'经流操作分派与写出函数到达 write；这里的 sync 并非 fsync。',25,GRAY)
d.line((40,631,1160,631),fill='#a5b5c3',width=2)
text(d,(45,650),'内核态：fd 查表找到打开的文件对象',27,TEAL)
box(d,(45,710,322,856),'files_struct','fdt')
box(d,(409,710,724,856),'fdtable','fd[1]：struct file *')
box(d,(811,710,1155,930),'struct file','f_pos：当前偏移\nf_inode：inode 指针\nf_mapping：缓存映射')
arrow(d,(324,781),(407,781));arrow(d,(726,781),(809,781))
box(d,(45,1000,360,1148),'inode','文件元数据')
box(d,(630,1000,1155,1148),'address_space','i_pages：页缓存索引')
d.line((807,843,768,843,768,960,500,960,500,1073,362,1073),fill=BLUE,width=3);arrow(d,(410,1073),(362,1073))
arrow(d,(981,932),(981,998),TEAL)
text(d,(45,1183),'页缓存可供其他进程读取；持久化还需要文件系统与设备完成同步。',26)
text(d,(45,1222),'图示省略锁、引用计数及具体文件系统路径。',24,GRAY)
watermark(d,1310);im.save(ART/'img-fflush-objects.png')

im,d=canvas(1000)
text(d,(45,28),'成功返回，要看确认的是哪一步',39)
text(d,(45,93),'两个目的地，后续需要的确认不同',26,GRAY)
box(d,(55,163,550,310),'普通文件：stdio 缓冲','fflush(fp) 成功',TEAL)
box(d,(650,163,1145,310),'管道：stdio 缓冲','fflush(fp) 成功',TEAL)
arrow(d,(303,312),(303,365),TEAL);arrow(d,(898,312),(898,365),TEAL)
box(d,(55,368,550,528),'内核接收字节','通常进入文件页缓存\n其他进程可以读到')
box(d,(650,368,1145,528),'内核管道缓冲有字节','接收端可能还没读\n本篇实验停在这里')
arrow(d,(303,530),(303,550));arrow(d,(898,530),(898,550))
arrow(d,(303,597),(303,608));arrow(d,(898,597),(898,608))
text(d,(78,557),'fsync(fd)，检查返回值',25,TEAL)
text(d,(691,557),'接收端读取并处理',25,TEAL)
box(d,(55,611,550,791),'获得文件同步确认','Linux 接口等待设备报告完成\n新建 / 改名还需同步目录')
box(d,(650,611,1145,791),'获得业务处理确认','接收端通过协议返回确认\n刷新本身不提供这份确认')
text(d,(55,841),'顺序：先 fflush，再 fsync；两步之间禁止并发追加本次待提交数据。',26)
text(d,(55,886),'实际耐久性仍需核对文件系统、设备与部署条件。',26,GRAY)
watermark(d,1000);im.save(ART/'img-flush-confirmations.png')
print('saved two diagrams')
