from pathlib import Path
import json, subprocess
art = Path(__file__).resolve().parent
prompt = '直接生成最终900×383横向技术公众号封面，比例900:383，浅米白底，深蓝和青色，少量橙色，精致扁平教学插画。主体居中，横向并排两个连续场景：左边一个读取机械手刚从文件槽取出最后一枚字节方块，旁边的结束指示灯仍熄灭；右边同一个机械手再次探入已经空的槽，没有取到方块，这时结束指示灯才亮起。用一根细箭头表达先后关系，图形清楚表现先尝试读取才能知道结束，不要把结束标记画成文件里的一枚字节。只允许两处文字：左下“标准 I/O 库 · 第7期”，右下“公众号·理解力笔记”。不加文章标题，不加其他标签和英文。文字和水印直接生成，边缘40像素留白。'
name='cover-21-feof-read-loop'
(art/'image-prompts.json').write_text(json.dumps({'name':name,'prompt':prompt},ensure_ascii=False,indent=2)+'\n')
with (art/(name+'.log')).open('w') as log:
 result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=log,stderr=subprocess.STDOUT)
print('cover generation exit:',result.returncode)
if result.returncode: raise SystemExit(result.returncode)
from PIL import Image
with Image.open(art/(name+'.png')) as im:
 im.convert('RGB').resize((900,383), Image.Resampling.LANCZOS).save(art/(name+'-900.png'))
print(art/(name+'-900.png'))
