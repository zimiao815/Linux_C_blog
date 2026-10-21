from pathlib import Path
import json, subprocess
art = Path(__file__).resolve().parent
prompt = '直接生成最终900×383横向技术公众号封面，比例900:383，浅米白底，深蓝青色与少量橙色，精致简洁教学插画。主体居中：左侧一个宽敞的双通道接收槽，上方通道接收蓝色字节方块，下方通道接收橙色结束标识，两种形状清楚分开；右侧一个狭窄通道把这两种不同输入挤压成完全相同的小方块，表达过早缩窄类型导致信息不可区分。箭头清楚，构图克制，不画电脑屏幕或磁盘，不加复杂线路。只允许两处文字：左下“标准 I/O 库 · 第8期”，右下“公众号·理解力笔记”。不加文章标题，不加英文数字和其他标签，所有文字与水印直接生成，边缘40像素留白。'
name='cover-22-fgetc-int'
(art/'image-prompts.json').write_text(json.dumps({'name':name,'prompt':prompt},ensure_ascii=False,indent=2)+'\n')
with (art/(name+'.log')).open('w') as log:
 result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=log,stderr=subprocess.STDOUT)
print('cover generation exit:',result.returncode)
if result.returncode: raise SystemExit(result.returncode)
from PIL import Image
with Image.open(art/(name+'.png')) as im:
 im.convert('RGB').resize((900,383), Image.Resampling.LANCZOS).save(art/(name+'-900.png'))
print(art/(name+'-900.png'))
