"""Run in a fresh temporary directory; leave no executable in the article folder."""
from pathlib import Path
import json, os, platform, subprocess, tempfile
art = Path(__file__).resolve().parent
flags = ['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records = {'system':platform.platform(),'compiler':subprocess.check_output(['cc','--version'],text=True),'flags':flags,'cases':[]}
with tempfile.TemporaryDirectory(prefix='article10-') as temp:
    root=Path(temp)
    sample=root/'sample'; sample.mkdir()
    (sample/'a.txt').write_text('hello\n')
    (sample/'.hidden').touch()
    (sample/'subdir').mkdir()
    (sample/'link').symlink_to('a.txt')
    (root/'empty').mkdir()
    subprocess.run(['cc',*flags,str(art/'list_dir.c'),'-o',str(root/'list_dir')],check=True,cwd=root)
    injected=(art/'list_dir.c').read_text().replace('int main(', 'struct dirent *injected_readdir(DIR *dir);\n\nint article_main(').replace('readdir(dir)', 'injected_readdir(dir)')
    (root/'list_dir_injected.c').write_text(injected)
    subprocess.run(['cc',*flags,'-c',str(root/'list_dir_injected.c'),'-o',str(root/'list_dir.o')],check=True,cwd=root)
    subprocess.run(['cc',*flags,str(art/'inject_readdir_error.c'),str(root/'list_dir.o'),'-o',str(root/'list_dir_fault')],check=True,cwd=root)
    for exe,arg,expected in [('list_dir','sample',0),('list_dir','empty',0),('list_dir','missing',1),('list_dir','sample/a.txt',1),('list_dir_fault','sample',1)]:
        r=subprocess.run(['./'+exe,arg],cwd=root,capture_output=True,text=True)
        assert r.returncode==expected,(exe,arg,r)
        if exe=='list_dir' and arg=='sample': assert set(r.stdout.splitlines())=={'a.txt','.hidden','subdir','link'}
        if arg=='empty': assert not r.stdout and not r.stderr
        if exe=='list_dir_fault': assert 'readdir sample:' in r.stderr and len(r.stdout.splitlines())==1
        record={'command':f'./{exe} {arg}','stdout':r.stdout,'stderr':r.stderr,'exit_status':r.returncode}
        records['cases'].append(record)
        print(json.dumps(record,ensure_ascii=False))
    env = dict(os.environ, READDIR_TEST_MODE='stale')
    r=subprocess.run(['./list_dir_fault','sample'],cwd=root,env=env,capture_output=True,text=True)
    assert r.returncode == 0 and not r.stderr
    assert set(r.stdout.splitlines()) == {'a.txt','.hidden','subdir','link'}
    records['cases'].append({'command':'READDIR_TEST_MODE=stale ./list_dir_fault sample','stdout':r.stdout,'stderr':r.stderr,'exit_status':r.returncode})
    print('stale errno test passed')
(art/'verification.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
