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

im,d=canvas(1330)
text(d,(45,25),'关闭流：先处理待写数据，再解除资源关联',37)
text(d,(45,86),'glibc 2.40 普通文件输出路径 / Linux v6.6 对象示意',25,TEAL)
text(d,(45,133),'用户态：关闭前',27,GRAY)
box(d,(45,185,495,396),'fp → FILE','_IO_write_base / _IO_write_ptr\n_fileno = fd')
box(d,(745,185,1155,396),'输出缓冲区','record=42 + 换行，共 10 字节\n自备数组仍由调用方持有',TEAL)
arrow(d,(497,283),(743,283),TEAL);text(d,(530,237),'缓冲指针',25,TEAL)
box(d,(45,448,355,597),'尝试刷新','可能在这里写入失败')
box(d,(445,448,755,597),'继续底层关闭','解除 fd 与文件的关联')
box(d,(845,448,1155,597),'清理流资源','返回后原流不可再用')
arrow(d,(357,521),(443,521));arrow(d,(757,521),(843,521))
text(d,(45,621),'普通文件路径保存刷新结果，仍执行关闭与清理；错误随后返回。',25,GRAY)
d.line((40,677,1160,677),fill='#a5b5c3',width=2)
text(d,(45,697),'内核态：关闭前的指向关系',27,TEAL)
box(d,(45,761,325,909),'files_struct','fdt')
box(d,(415,761,745,909),'fdtable','fd[fd]：struct file *')
box(d,(835,761,1155,982),'struct file','f_pos：当前偏移\nf_inode：inode 指针\nf_op：文件操作')
arrow(d,(327,834),(413,834));arrow(d,(747,834),(833,834))
box(d,(835,1052,1155,1177),'inode','文件元数据')
arrow(d,(994,984),(994,1050))
text(d,(45,1015),'close 释放 fd 表项，编号可以被复用。',27)
text(d,(45,1063),'struct file 的寿命还取决于其他引用。',27)
text(d,(45,1111),'关闭一个流，不代表 inode 立即消失。',27)
text(d,(45,1228),'自动分配的流缓冲会释放；调用方提供的数组只解除关联。',26,GRAY)
watermark(d,1330);im.save(ART/'img-fclose-objects.png')

im,d=canvas(1080)
text(d,(45,28),'返回值和流的寿命，要分别处理',39)
box(d,(230,135,970,274),'写入或显式刷新','任何一步失败：记录原因，保留整体失败状态')
arrow(d,(600,276),(600,328))
box(d,(230,331,970,473),'唯一拥有者调用一次 fclose','保存失败原因；关闭后不再访问原流',TEAL)
d.line((600,475,600,515,300,515,300,554),fill=BLUE,width=4)
d.line((600,515,900,515,900,554),fill=BLUE,width=4)
arrow(d,(300,540),(300,554));arrow(d,(900,540),(900,554))
box(d,(55,557,550,723),'返回 0','本次关闭成功\n保留之前已经发生的失败')
box(d,(650,557,1145,723),'返回 EOF','报告关闭错误\n整体操作按失败处理')
d.line((300,725,300,774,600,774),fill=BLUE,width=4)
d.line((900,725,900,774,600,774),fill=BLUE,width=4)
arrow(d,(600,774),(600,820))
box(d,(230,823,970,950),'两条分支：原流均不可再用','不再 fclose、ferror、fileno；其他别名也必须停用',TEAL)
text(d,(55,987),'关闭清理不撤销已写内容；部分文件如何恢复，由保存协议决定。',26,GRAY)
watermark(d,1080);im.save(ART/'img-fclose-lifetime.png')
print('saved two diagrams')
