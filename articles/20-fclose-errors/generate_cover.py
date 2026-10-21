from pathlib import Path
import json, subprocess
art = Path(__file__).resolve().parent
prompt = '直接生成最终900×383横向技术公众号封面，比例900:383，浅米白底，深蓝和青色，少量橙红色，精致扁平教学插画。主体居中，左侧透明缓冲盒里有一行字节小方块，左侧入口旁一个小对勾表示已经收下；中间出口处是关闭动作触发的最后一次排出，有几个字节方块向右走，到达右侧文件容器前遇到红色阻挡标记；右下有一枚已经解除连接的插头，表达写出失败但连接使用期也结束。布局简洁，强调缓冲接收成功与关闭阶段写出失败的先后关系。只允许两处文字：左下“标准 I/O 库 · 第6期”，右下“公众号·理解力笔记”。不加文章标题，不加其他标签或数字，不画磁盘落盘确认。文字和水印直接生成，不留后期叠字区域。边缘40像素留白。'
name='cover-20-fclose-errors'
(art/'image-prompts.json').write_text(json.dumps({'name':name,'prompt':prompt},ensure_ascii=False,indent=2)+'\n')
with (art/(name+'.log')).open('w') as log:
 result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=log,stderr=subprocess.STDOUT)
print('cover generation exit:',result.returncode)
if result.returncode: raise SystemExit(result.returncode)
from PIL import Image
with Image.open(art/(name+'.png')) as im:
 im.convert('RGB').resize((900,383), Image.Resampling.LANCZOS).save(art/(name+'-900.png'))
print(art/(name+'-900.png'))
