from pathlib import Path
import json,os,subprocess
art=Path(__file__).resolve().parent
name='fclose-buffer-failure-ai-v2'
prompt='''只修正这张教学图中的数据字节数，保留整张图的版式、标题、字体、所有箭头、用户态和内核态边界、所有其他文字和右下水印。
必须修正：C 字符串 record=42 后带一个换行，实际总共 10 字节，不是 9 字节。将顶部“暂存 9 字节”改成“暂存 10 字节”。上下两个输出缓冲区都改画为 10 个小格，依次写 r、e、c、o、r、d、=、4、2、LF；其中最后一格 LF 表示一个换行字节。不能保留 a 到 i，不要把 LF 分成两个格。适当增宽容器以容纳十格，格内字符居中，箭头不要压住文字。顶层仍表示 fputs 成功，底层仍表示 write 被大小上限 0 拒绝，write 返回 -1 且 errno=EFBIG，fclose 最终返回 EOF。必须完整保留原图底部说明“本图只展开 fclose 的刷新阶段，关闭与清理仍会继续。”不要添加额外文字。'''
(art/(name+'-prompt.json')).write_text(json.dumps({'name':name,'prompt':prompt,'source':str(art/'fclose-buffer-failure-ai.png')},ensure_ascii=False,indent=2)+'\n')
env=os.environ.copy();env['IMAGE_OUTPUT_DIR']=str(art/'.imagegen'/name/'outputs')
with (art/(name+'.log')).open('w') as log:
    run=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','edit','--json','--name',name,'--image',str(art/'fclose-buffer-failure-ai.png'),'--output',str(art/(name+'.png')),'--prompt',prompt],cwd=art.parents[2]/'linux_c_blog_workflow',env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900)
print('image correction exit:',run.returncode,flush=True)
raise SystemExit(run.returncode)
