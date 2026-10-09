from pathlib import Path
import json, subprocess, concurrent.futures
art=Path(__file__).resolve().parent
style='为中文 Linux C 教程生成准确、清晰的技术示意图。白色或极浅灰背景，深蓝字，青色和橙色辅助，大字，移动端可读。只画指定关系，不添加无关箭头。所有文字由 AI 直接生成。右下角水印“公众号·理解力笔记”。'
jobs=[
('cover-12-mkdir-multilevel', '生成横向封面，宽高比900:383。主体居中：三层目录树 a / b / c，左侧 a 和 b 的目录卡片逐级亮起，右侧 c 从问号变成新建目录，清晰表现递归创建多级目录。克制的蓝青色科技教学风格，无人物无装饰电路。文字只能有左下“文件与目录·第5期”和右下“公众号·理解力笔记”，不写文章标题或技术单词。'),
('img-mkdir-path',style+'''横向4:3，标题“mkdir 只创建最后一个路径分量”。画一条从左到右的路径解析流程：当前目录或根目录 → 目录 a → 目录 b → 待创建目录 c。前三个框标注“父目录必须已存在”，最后一个框标注“mkdir 创建这一项”。下方用红色错误分支表现：若 a 或 b 不存在，返回 ENOENT；若 b 是普通文件，返回 ENOTDIR。只表达路径分量逐级解析，不画文件内容和 inode 内部细节。'''),
('img-mkdir-state',style+'''纵向4:5，标题“递归创建把一个目标拆成多个前缀”。从顶部目标路径“/tmp/app/cache/logs”向下分成四个依次执行的状态框：mkdir("/tmp", 0777)（已存在，确认目录）、mkdir("/tmp/app", 0777)（新建）、mkdir("/tmp/app/cache", 0777)（新建）、mkdir("/tmp/app/cache/logs", 0777)（新建）。每个框右侧小标签只能是“EEXIST → stat 确认目录”或“mkdir 成功”。底部加一条失败支路“已有名字是普通文件 → ENOTDIR”。箭头按从上到下顺序，布局简单清楚。'''),
('img-mkdir-race',style+'''纵向4:5，标题“路径循环能工作，但不等于安全创建”。左右两列对比。左列标题“普通路径循环”，流程：mkdir(prefix) → EEXIST → stat(prefix) 是目录 → 继续下一级；旁边标注“适合普通初始化和测试夹具”。右列标题“路径可被替换时”，流程：stat 看到目录 → 另一个进程替换名字 → 下一次按路径解析到不同对象；底部红色警示“存在 TOCTOU 窗口”。最下方蓝色建议框“需要固定起点时：目录 fd + mkdirat”。不要画复杂内核结构，不要暗示 mkdirat 自动递归。''')]
(art/'image-prompts.json').write_text(json.dumps([{'name':n,'prompt':p,'output':n+'.png'} for n,p in jobs],ensure_ascii=False,indent=2))
def run(job):
 n,p=job
 cmd=['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',n,'--output',str(art/(n+'.png')),'--prompt',p]
 with (art/(n+'.log')).open('w') as out:
  r=subprocess.run(cmd,cwd=art.parents[2]/'linux_c_blog_workflow',stdout=out,stderr=subprocess.STDOUT)
 return n,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for result in ex.map(run,jobs): print(result,flush=True)
