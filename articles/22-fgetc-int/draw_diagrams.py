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

im,d=canvas(800)
text(d,(45,25),'两种 char，都可能合并原本不同的结果',36)
text(d,(45,85),'本机实测：8 位 char，EOF = -1；有符号转换结果不作跨平台承诺',24,GRAY)
text(d,(58,151),'有符号 char',32,BLUE)
text(d,(660,151),'无符号 char',32,TEAL)
box(d,(50,222,540,359),'有效字节：int 255','文件中的 FF，尚未遇到结束')
box(d,(50,409,540,546),'结束状态：int -1','这次没有读到字节')
box(d,(660,222,1150,359),'有效字节：int 255','转换后仍为 255',TEAL)
box(d,(660,409,1150,546),'结束状态：int -1','转换后也变为 255',TEAL)
d.line((50,290,27,290,27,584,180,584),fill=BLUE,width=3)
arrow(d,(180,584),(180,608));arrow(d,(410,548),(410,608))
d.line((1152,290,1173,290,1173,584,790,584),fill=TEAL,width=3)
arrow(d,(790,584),(790,608),TEAL);arrow(d,(1020,548),(1020,608),TEAL)
box(d,(50,610,540,718),'char 结果都变为 -1','字节 FF 可能被误判为 EOF')
box(d,(660,610,1150,718),'char 结果都变为 255','EOF 可能被当成字节继续处理',TEAL)
watermark(d,800);im.save(ART/'img-char-collision.png')

im,d=canvas(1120)
text(d,(45,25),'先保留 int，识别 EOF 后再按需缩窄',37)
text(d,(45,86),'glibc 2.40 用户态缓冲路径示意；不是内存现场或内核调用图',24,GRAY)
box(d,(45,157,525,364),'fp → FILE','_IO_read_ptr\n_IO_read_end\n_flags：结束 / 错误标志')
box(d,(775,175,1155,348),'输入缓冲中的 FF','按 unsigned char 取值\n得到 255',TEAL)
arrow(d,(527,253),(773,253),TEAL);text(d,(570,208),'指针',25,TEAL)
box(d,(220,431,980,574),'fgetc 返回 int','字节：0…255；结束或错误：EOF（本机为 -1）')
arrow(d,(964,350),(964,429),TEAL)
text(d,(330,382),'结束 / 错误由库返回 EOF',25,GRAY)
arrow(d,(285,366),(285,429))
arrow(d,(600,576),(600,632))
box(d,(350,635,850,752),'先比较 ch 与 EOF','保留区分字节和状态的机会',TEAL)
d.line((600,754,600,795,295,795,295,833),fill=BLUE,width=4)
d.line((600,795,905,795,905,833),fill=BLUE,width=4)
arrow(d,(295,817),(295,833));arrow(d,(905,817),(905,833))
box(d,(45,836,545,989),'ch == EOF','通过 ferror / feof 判别原因\n不把它存进字节数组')
box(d,(655,836,1155,989),'ch != EOF','按需转成 unsigned char\n或直接交给接收 int 的 fputc',TEAL)
text(d,(45,1030),'先转 char 再转回 int，无法恢复已经合并的两种结果。',27,GRAY)
watermark(d,1120);im.save(ART/'img-fgetc-order.png')
print('saved two diagrams')
