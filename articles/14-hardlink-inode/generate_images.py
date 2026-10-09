from pathlib import Path
import json, subprocess, concurrent.futures
art=Path(__file__).resolve().parent
style='中文 Linux C 技术教程，纯白不透明背景，深蓝大字，青色和橙色辅助，结构准确，移动端可读，右下角水印“公众号·理解力笔记”。不要添加未指定关系。'
jobs=[
('cover-14-hardlink-inode','生成最终横向900×383封面，比例900:383。主体居中：两个不同文件名标签“name A”和“name B”通过两条蓝色连线指向同一个发光的 inode/文件数据卡片，旁边有一个被划掉的旧名字但数据卡片仍保留，表达硬链接共享 inode 和删除一个名字后对象仍在。蓝青色技术教学风格，无人物。文字只能有左下“文件与目录·第7期”和右下“公众号·理解力笔记”，不要文章标题。'),
('img-hardlink-objects',style+'''横向4:3，标题“多个名字，共享一个 inode”。上方父目录框中有两个目录项“nameA”和“nameB”，两条箭头都指向下方同一个“inode”框。inode 框内显示“i_ino”“i_nlink = 2”“文件类型和权限”，再向右指向“文件数据块”。在 inode 旁边放注释“名字不同，st_dev + st_ino 相同”。不要画两个 inode，不要把目录项画成数据副本，不要把 i_nlink 写成打开进程数。'''),
('img-hardlink-lifecycle',style+'''纵向4:5，标题“删除一个名字，文件对象还在”。分三步状态：步骤1，父目录中 nameA、nameB 都指向同一 inode，标 i_nlink=2；步骤2，unlink(nameA) 用红叉移除 nameA，nameB 仍指向 inode，标 i_nlink=1；步骤3，unlink(nameB) 移除最后名字，旁边仍有“进程 fd=3”箭头指向 struct file，再指向 inode，标“无目录名字，但 fd 仍可读”。最后 fd 关闭后用灰色虚线表示对象可回收。明确区分目录名字、inode 和打开 fd，不画 fd 直接指向目录项。'''),
('img-hardlink-path',style+'''纵向4:5，标题“硬链接的限制来自文件系统和对象类型”。顶部应用层“link(oldpath, newpath)”和“linkat(dirfd, old, new, flags)”两个接口。向下分三条错误/边界分支：分支一“oldpath 与 newpath 不在同一文件系统”→“EXDEV”；分支二“newpath 已存在”→“EEXIST”；分支三“目标是目录（通常禁止）”→“EPERM”。成功分支到底部“同一文件系统中新增目录项，inode 链接计数 +1”。不要把跨文件系统错误写成 ENOENT，不要画递归复制文件内容。''')]
(art/'image-prompts.json').write_text(json.dumps([{'name':n,'prompt':p} for n,p in jobs],ensure_ascii=False,indent=2)+'\n')
def run(job):
 n,p=job
 with (art/(n+'.log')).open('w') as f:
  r=subprocess.run(['python3','/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py','generate','--json','--name',n,'--output',str(art/(n+'.png')),'--prompt',p],cwd=art.parents[2]/'linux_c_blog_workflow',stdout=f,stderr=subprocess.STDOUT)
 return n,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for r in pool.map(run,jobs): print(r,flush=True)
