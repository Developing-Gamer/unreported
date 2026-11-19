"""Factory v3 totals per system. A rerun job (f3r-*, f3cr-*) replaces the original trial of the same task."""
import json,sys,re,collections
rows=[r for f in sys.argv[1:] for r in json.load(open(f))]
def system(job): return re.sub(r'-(p|h|q|e|x|y|t|u|w)?\d+$','',re.sub(r'-?b-p','-p',re.sub(r'^f3x([co]?)-',r'f3\1-',re.sub(r'^f(\d)([co]?)r-',r'f\1\2-',job))))
best={}
for r in rows:
    k=(system(r['job']),r['task']); rerun=bool(re.match(r'^f\dc?o?r-',r['job']))
    if k not in best or rerun: best[k]=r
agg=collections.defaultdict(list)
for (s,_),r in best.items(): agg[s].append(r)
print(f"{'system':16} tasks reported hidden  total   wontfix-acted  FP(all)  PR")
for k,rs in sorted(agg.items()):
    rep=sum(r['resolved'] for r in rs); hid=sum(len(r.get('hidden_fixed',[])) for r in rs); ht=sum(r.get('hidden_total',0) for r in rs)
    wf=sum(len(r.get('wontfix_acted',[])) for r in rs); wt=sum(r.get('wontfix_total',0) for r in rs)
    fp=sum(len(r['false_positives']) for r in rs); pr=[r['judge']['total'] or 0 for r in rs]
    print(f"{k:16} {len(rs):5} {rep:4}/{len(rs)} {hid:3}/{ht}  {rep+hid:3}/{len(rs)+ht}   {wf}/{wt}          {fp:3}   {sum(pr)/len(pr):.1f}")
