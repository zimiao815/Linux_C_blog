from pathlib import Path
import concurrent.futures, json, os, subprocess
art = Path(__file__).resolve().parent
common = '''为中文 C 编程公众号制作一张准确、易读的教学图，纯白背景，蓝色表示用户态，青色表示正常路径，橙红色表示失败。现代扁平矢量信息图风格，不画立体硬件，不用装饰性科技背景。横向画布约 1536×1024，四周留白，简体中文无衬线字体大而清晰，手机上也能读懂。所有文字必须严格按下列要求，英文函数名大小写正确。对象少，箭头不交叉，不穿过文字。右下角水印“公众号·理解力笔记”。'''
prompts = {
'fclose-buffer-failure-ai': common + '''标题“为什么写入成功，关闭却失败？”；副标题“文件大小上限为 0 的实验”。主体按上、下两个宽面板排列。
上面板标题“① fputs：先存入内存”。左边一个 fputs(data, fp) 标签，绿色箭头指向右边一个大容器，容器标题“用户态输出缓冲”，画九个简洁字节格，容器旁短注“暂存 9 字节”。箭头上标“写入缓冲”；右下角绿色结果“fputs 返回成功”。这一阶段不要画通向内核或文件的箭头。
下面板标题“② fclose：刷新缓冲时失败”。面板用一条竖虚线分成左侧“用户态”和右侧“内核态”。左侧上方写“fclose 调用写出操作”，下面画同样的缓冲容器，标签“FILE → 输出缓冲”。从缓冲向右画跨越虚线的蓝色实线箭头，箭头标“write(fd, ...)”。右侧画单个大框标题“内核检查文件大小上限”，框内两行“上限为 0”“拒绝写入”，红色阻挡图形。框下方小注“文件仍为 0 字节”。从右侧框返回左侧的下方单独红色箭头，沿下方水平返回，不与前向箭头相交，箭头上标“write 返回 -1，errno = EFBIG”。左端红色结果框“fclose 最终返回 EOF”。底部小注“本图只展开 fclose 的刷新阶段，关闭与清理仍会继续。”
不要添加 inode、磁盘、复杂结构体表、其他语句，不把 EOF 标在系统调用 write 的返回箭头上。''',
'fclose-check-once-ai': common + '''标题“两次检查，一次关闭”。用从上到下的清楚流程说明应用程序的错误处理，只放四层，不画内核图。
第一层一个蓝色宽框“调用 fputs，记录写入结果”。下方蓝色箭头，旁边只标“无论写入成功还是失败”。
第二层一个青色宽框“调用一次 fclose，记录关闭结果”。下方箭头分为左右两支。
第三层左侧绿色框标题“两次都成功”，内容“本次保存成功”；右侧橙红色框标题“任意一次失败”，内容“本次保存失败”。每个框内部只有这两行文字。
第四层在底部画一个横跨画面的浅橙色提醒栏，标题“fclose 返回后，原流不可再用”，下一行“不重试 fclose，不再用原来的 fp 读取或写入”。这个提醒适用于左右两种结果，用两条细线从左右结果框接到提醒栏。最下方小字“保存成功不等于数据已持久化到磁盘”。
重点：第一层的失败也必须进入第二层；不要画写入失败后直接跳到最终结果的箭头；不要画 fclose 的重试环。不要添加函数内部名称、代码表格或其他装饰。'''
}
(art/'explanation-image-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2)+'\n')
def generate(item):
    name,prompt=item
    env=os.environ.copy()
    env['IMAGE_OUTPUT_DIR']=str(art/'.imagegen'/name/'outputs')
    with (art/(name+'.log')).open('w') as log:
        result=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',name,'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900)
    return dict(name=name,exit=result.returncode,path=str(art/(name+'.png')))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(generate,prompts.items()))
(art/'explanation-image-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False),flush=True)
assert all(r['exit']==0 for r in results)
