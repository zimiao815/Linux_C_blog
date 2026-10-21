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

im,d=canvas(1450)
text(d,(45,25),'feof / ferror 查询 FILE 中的状态标志',37)
text(d,(45,86),'普通文件缓冲读：glibc 2.40 / Linux v6.6 源码示意',25,TEAL)
text(d,(45,133),'用户态：查询标志本身，不尝试读取新字节',27,GRAY)
box(d,(45,185,555,462),'fp → FILE','_flags：EOF / error 两个标志\n_IO_read_base / _IO_read_ptr\n_IO_read_end\n_fileno = fd')
box(d,(785,208,1155,434),'输入缓冲区','尚未消费的字节\n[read_ptr, read_end)',TEAL)
arrow(d,(557,316),(783,316),TEAL);text(d,(594,268),'缓冲指针',25,TEAL)
box(d,(45,510,1155,658),'缓冲不足，且尚未记录 EOF 时，才继续补充','fgetc 经 _IO_new_file_underflow 等路径，调用底层 read')
d.line((40,710,1160,710),fill='#a5b5c3',width=2)
text(d,(45,730),'内核态：read 使用 fd 查找打开的文件对象',27,TEAL)
box(d,(45,790,325,934),'files_struct','fdt')
box(d,(415,790,745,934),'fdtable','fd[fd]：struct file *')
box(d,(835,790,1155,1000),'struct file','f_pos：当前偏移\nf_inode：inode 指针\nf_op：文件操作')
arrow(d,(327,860),(413,860));arrow(d,(747,860),(833,860))
box(d,(835,1060,1155,1177),'inode','文件元数据')
arrow(d,(994,1002),(994,1058))
text(d,(45,1005),'read 的结果返回用户态，库据此更新流。',26)
text(d,(45,1058),'read 返回 0 与 fgetc 返回 EOF 是不同层的结果。',25,GRAY)
text(d,(45,1120),'下面三格仅描述本次补充缓冲的分支：',25,TEAL)
box(d,(45,1224,375,1370),'read > 0','填充缓冲\n返回一个字节')
box(d,(435,1224,765,1370),'read == 0','置 _IO_EOF_SEEN\n返回 EOF',TEAL)
box(d,(825,1224,1155,1370),'read < 0','置 _IO_ERR_SEEN\n返回 EOF')
watermark(d,1450);im.save(ART/'img-feof-objects.png')

im,d=canvas(1130)
text(d,(45,28),'让读取结果决定是否处理数据',39)
text(d,(45,92),'适用本篇：新打开的流，由一个读取者管理状态',25,GRAY)
box(d,(350,158,850,287),'ch = fgetc(fp)','先尝试读取',TEAL)
d.line((600,289,600,331,270,331,270,380),fill=BLUE,width=4)
d.line((600,331,930,331,930,380),fill=BLUE,width=4)
arrow(d,(270,365),(270,380));arrow(d,(930,365),(930,380))
box(d,(55,383,485,525),'ch != EOF','处理本次读到的字节')
box(d,(715,383,1145,525),'ch == EOF','停止处理，检查状态')
d.line((55,454,26,454,26,136,600,136),fill=TEAL,width=4)
arrow(d,(600,136),(600,156),TEAL)
text(d,(63,558),'处理完，再调用读取函数',26,TEAL)
arrow(d,(930,527),(930,615))
box(d,(715,618,1145,758),'先看 ferror(fp)','非零就报告读取错误')
d.line((715,686,580,686,580,806),fill=BLUE,width=4)
arrow(d,(580,790),(580,806));text(d,(600,636),'为 0',24,GRAY)
box(d,(255,809,905,951),'无读取错误：按正常结束处理','本篇前提下成立；随后检查输出与资源')
text(d,(55,995),'EOF 是返回值；feof / ferror 是流的历史状态，二者不能替换。',26)
watermark(d,1130);im.save(ART/'img-read-result-loop.png')
print('saved two diagrams')
