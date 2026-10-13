from pathlib import Path
import json, subprocess
art = Path(__file__).resolve().parent
prompt = '直接生成最终900×383横向技术公众号封面，比例900:383，浅米白底，深蓝、青色、少量橙色，精致扁平教学图。主体居中分成左右对照：左侧一个用户态小缓冲盒中的一行字节方块通过箭头到达终端屏幕，屏幕出现青色的一行短横线；右侧同样的一行字节方块仍停在用户态缓冲盒中，下方文件卡片为空白，连接箭头以虚线表示尚未输出。明确表达终端即时看到一行而重定向文件尚无输出，不画物理磁盘，不画时间长短仪表。只允许两处文字：左下“标准 I/O 库 · 第3期”，右下“公众号·理解力笔记”。不加文章标题，不加其他标签。文字和水印直接生成，不留后期叠字区域。边缘40像素留白，内容完整。'
name='cover-17-stdout-buffering'
(art/'image-prompts.json').write_text(json.dumps({'name':name,'prompt':prompt},ensure_ascii=False,indent=2)+'\n')
with (art/(name+'.log')).open('w') as log:
 result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=log,stderr=subprocess.STDOUT)
print('cover generation exit:',result.returncode)
if result.returncode: raise SystemExit(result.returncode)
from PIL import Image
with Image.open(art/(name+'.png')) as im:
 im.convert('RGB').resize((900,383), Image.Resampling.LANCZOS).save(art/(name+'-900.png'))
print(art/(name+'-900.png'))
