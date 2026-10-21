from pathlib import Path
import json, subprocess
art = Path(__file__).resolve().parent
prompt = '直接生成最终900×383横向技术公众号封面，比例900:383，浅米白底，深蓝、青色、少量橙色，精致扁平教学图。主体居中，从左到右三个对象：左侧是装着字节小方块的透明用户缓冲容器，中央是接住字节的内存托盘，右侧是磁盘。左到中的实线箭头清楚表示字节已送达内存托盘，中到磁盘使用细虚线且没有完成对勾，表示仍需独立的保存步骤。不要画成直达磁盘的连续实线。只允许两处文字：左下“标准 I/O 库 · 第5期”，右下“公众号·理解力笔记”。不加文章标题，不加其他标签。文字和水印直接生成，不留后期叠字区域。边缘40像素留白，内容完整。'
name='cover-19-fflush-boundaries'
(art/'image-prompts.json').write_text(json.dumps({'name':name,'prompt':prompt},ensure_ascii=False,indent=2)+'\n')
with (art/(name+'.log')).open('w') as log:
 result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=log,stderr=subprocess.STDOUT)
print('cover generation exit:',result.returncode)
if result.returncode: raise SystemExit(result.returncode)
from PIL import Image
with Image.open(art/(name+'.png')) as im:
 im.convert('RGB').resize((900,383), Image.Resampling.LANCZOS).save(art/(name+'-900.png'))
print(art/(name+'-900.png'))
