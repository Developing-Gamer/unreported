import sys, re, subprocess, os
B=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
ANSI=re.compile(r'\x1b\[[0-9;]*m')
CUT=re.compile(r'^(Updated \d+ paths? from|Downloading |Downloaded |Installed \d|Resolved \d|Prepared \d|SWEBench results|  × Failed|warning: )')
def grade(d):
    task=d.rstrip('/').split('/')[-1].rsplit('__',1)[0]
    lines=[ANSI.sub('',l) for l in open(d+'verifier/test-stdout.txt',errors='ignore')]
    starts=[i for i,l in enumerate(lines) if l.strip()=='+ set +x']
    if not starts: return 'NOSTART'
    out=[]
    for l in lines[starts[-1]+1:]:
        if CUT.match(l): break
        out.append(l)
    log=f'log-{os.path.basename(d.rstrip("/"))}.txt'; open(log,'w').write(''.join(out))
    r=subprocess.run(['uv','run','-q',os.path.join(os.path.dirname(os.path.abspath(__file__)),'grade.py'),B+f'factory/v3f/tasks/{task}/tests/config.json',log],capture_output=True,text=True)
    return r.stdout.strip() or r.stderr.strip()[-200:]
for d in sys.argv[1:]:
    print(os.path.basename(d.rstrip('/')), 'reward', open(d+'verifier/reward.txt').read().strip(), '->', grade(d), flush=True)
