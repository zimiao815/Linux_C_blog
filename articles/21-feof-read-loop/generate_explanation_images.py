from pathlib import Path
import concurrent.futures,json,os,subprocess
art=Path(__file__).resolve().parent
common='''为中文 C 编程公众号制作一张简洁清晰的技术教学图，1536×1024 横向画布，纯白背景，深蓝标题，蓝色表示用户态，青色表示正常状态，橙红色表示错误。大号简体中文无衬线字，保持充足留白，扁平矢量图风格。严格按指定文字写，不额外发明代码或标签。箭头不相交、不穿文字。右下角必须有水印“公众号·理解力笔记”。不要画装饰性电脑或磁盘插画。'''
prompts={
'feof-timing-ai':common+'''标题“读到最后一个字节，不等于已经发现结束”；副标题“文件只有一个字节 A，新打开的输入流”。主体为三个从左向右排列的宽大卡片，卡片用粗蓝箭头连接，每张卡片各有时间编号。
左卡片标题“① 尚未读取”；卡片内画一个简洁的文件框，只含字母 A；下面写“尚未调用 fgetc”；底部写“feof = 0”。
中卡片标题“② 第一次读取”；写“fgetc 返回 65（A）”；下面画字母 A 已被取出的简洁示意，不画 EOF 字节；底部写“feof = 0”。
右卡片标题“③ 再读一次”；写“fgetc 返回 EOF”；下面写“这次没有读到字节”；底部用青色突出“feof = 1”。
卡片下方用一条较大的说明栏写“feof 记录已经发现的结束，不预测下一次读取。”；再下一行小字“本图只讨论正常读完；标志按 0 / 1 表示。”
务必保证第一次取到 A 后仍为 0，第二次返回 EOF 后才为 1。不要画文件中存在 EOF 字节，不画错误循环，不把数字 65 写成字节计数。''',
'feof-return-ai':common+'''标题“同样返回 EOF，停止原因可能不同”；副标题“新打开的普通文件流：首次遇到结束或读取错误”。
主体做成两行、三列的技术关系图，列标题从左到右依次为“内核读取结果”“C 库更新 FILE 状态”“fgetc 返回值”。左列与中列之间用竖虚线分隔，虚线上方标小字“内核态 / 用户态”。
第一行青色：左框“read 返回 0”，第二行小字“没有更多数据”；实线箭头指向中框“EOF 标志 = 1”及“错误标志 = 0”；中框再用箭头指向右框“EOF”。
第二行橙红色：左框“read 返回 -1”，第二行小字“读取发生错误”；实线箭头指向中框“EOF 标志 = 0”及“错误标志 = 1”；中框再用箭头指向右框“EOF”。
两行之间保持足够留白。主体下方说明栏写“停止后检查 ferror，不能只凭 EOF 判断成功。”
最下方两行较小但清晰的注释：“仅展示补充缓冲时的两个停止分支。”及“缓冲中有数据时，fgetc 可以直接取字节，不必每次调用 read。”
不要绘制 FILE 内部字段名、inode 或多余节点；不要把内核 read 返回值写成 EOF；不要暗示结束和错误标志在所有历史状态下一定互斥。'''
}
(art/'explanation-image-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2)+'\n')
def run(item):
    name,prompt=item
    env=os.environ.copy();env['IMAGE_OUTPUT_DIR']=str(art/'.imagegen'/name/'outputs')
    with (art/(name+'.log')).open('w') as log:
        p=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900)
    return dict(name=name,exit=p.returncode,path=str(art/(name+'.png')))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,prompts.items()))
(art/'explanation-image-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False),flush=True)
assert all(r['exit']==0 for r in results)
