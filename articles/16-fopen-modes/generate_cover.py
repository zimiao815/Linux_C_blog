from pathlib import Path
import json, subprocess
art = Path(__file__).resolve().parent
prompt = '''直接生成最终 900×383 横向公众号封面，长宽比900:383。干净浅米白背景，深蓝、青色、橙色，精致扁平技术教学风格。主题是打开文件的三种选择：主体居中横排三个文件卡片。左侧卡片保留三行蓝色已有内容，一枚放大镜表示读取；中间卡片从三行旧内容被擦除变成空白纸页，橙色橡皮和短箭头表示打开时清空；右侧卡片保留三行蓝色旧内容，末尾增加一行青色新内容，向下的小箭头表示追加。图形清晰，不用装饰性数据流。整幅只允许两处文字：左下“标准 I/O 库 · 第2期”，右下“公众号·理解力笔记”。禁止文章标题，禁止额外英文标签。所有文字由模型直接生成，四周留白至少40像素，主体居中。'''
name='cover-16-fopen-modes'
(art/'image-prompts.json').write_text(json.dumps({'name':name,'prompt':prompt},ensure_ascii=False,indent=2)+'\n')
with (art/(name+'.log')).open('w') as log:
 result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=log,stderr=subprocess.STDOUT)
print('cover generation exit:',result.returncode)
if result.returncode: raise SystemExit(result.returncode)
from PIL import Image
with Image.open(art/(name+'.png')) as im:
 im.convert('RGB').resize((900,383), Image.Resampling.LANCZOS).save(art/(name+'-900.png'))
print(art/(name+'-900.png'))
