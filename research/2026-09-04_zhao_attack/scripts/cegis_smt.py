from pathlib import Path
import sys,json,time,random,collections,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'local_deps'))
import z3

def negcode(a):
    out=0;p=1
    for _ in range(4):out+=((-a)%5)*p;a//=5;p*=5
    return out

def sums(seq):
    out=[(0,0,0)]
    for i,g in enumerate(seq):
        extra=[]
        for s,w,mask in out:
            ss=sum(((s//(5**j)+g[j])%5)*(5**j) for j in range(4))
            extra.append((ss,w+1,mask|(1<<i)))
        out+=extra
    return out

def witnesses(seq,m):
    h=len(seq)//2; ls=sums(seq[:h]);rs=sums(seq[h:]);by=collections.defaultdict(list)
    for s,w,mask in rs:by[s].append((w,mask))
    ans=[]
    for s,w,mask in ls:
      for ww,mm in by[negcode(s)]:
        if 0<w+ww<=m:ans.append((w+ww,mask|(mm<<h)))
    return sorted(ans)

def run(N,m,seconds,affine=False,bv=False):
    X=[[(z3.BitVec(f'x{i}_{j}',7) if bv else z3.Int(f'x{i}_{j}')) for j in range(4)] for i in range(N)]
    solver=z3.SolverFor('QF_BV') if bv else z3.Solver();solver.set(timeout=15000)
    mod5=lambda x:z3.URem(x,5) if bv else x%5
    for i in range(N):
      for j in range(4):
        solver.add(z3.ULE(X[i][j],4) if bv else z3.And(X[i][j]>=0,X[i][j]<=4))
      solver.add(z3.Or(*[v!=0 for v in X[i]]))
      if affine:solver.add(mod5(z3.Sum(X[i]))==1)
    for i in range(4):
      for j in range(4):solver.add(X[i][j]==(1 if i==j else 0))
    codes=[sum((5**j)*(z3.ZeroExt(3,X[i][j]) if bv else X[i][j]) for j in range(4)) for i in range(N)]
    for i in range(4,N-1):solver.add(z3.ULE(codes[i],codes[i+1]) if bv else codes[i]<=codes[i+1])
    for i in range(4,N-3):solver.add(z3.ULT(codes[i],codes[i+3]) if bv else codes[i]<codes[i+3])
    for b in (1,5,25,125):solver.add(z3.Sum([z3.If(codes[i]==b,1,0) for i in range(4,N)])<=2)
    rnd=random.Random(723);cut_masks=set();start=time.time();it=0;last=None
    ev=ROOT/'evidence';ev.mkdir(exist_ok=True)
    label=f'cegis_{N}'+('_affine' if affine else '_full')+('_bv' if bv else '')
    logfile=open(ev/f'{label}.log','w',encoding='utf-8')
    def emit(obj):
      line=json.dumps(obj);print(line,flush=True);logfile.write(line+'\n');logfile.flush()
    while time.time()-start<seconds:
      it+=1;status=solver.check()
      if status!=z3.sat:
        emit({'iteration':it,'status':str(status),'reason':solver.reason_unknown() if status==z3.unknown else '', 'cuts':len(cut_masks),'seconds':time.time()-start})
        break
      model=solver.model();seq=[[model.eval(v).as_long() for v in row] for row in X]
      ws=witnesses(seq,m);last=seq
      if not ws:
        (ev/f'{label}_candidate.json').write_text(json.dumps({'N':N,'m':m,'sequence':seq},indent=2),encoding='utf-8')
        emit({'iteration':it,'status':'CANDIDATE','cuts':len(cut_masks),'seconds':time.time()-start});break
      chosen=ws[:50]+rnd.sample(ws,min(100,len(ws)))
      for weight,mask in chosen:
        if mask in cut_masks:continue
        cut_masks.add(mask);idx=[i for i in range(N) if mask>>i&1]
        solver.add(z3.Or(*[mod5(z3.Sum([X[i][j] for i in idx]))!=0 for j in range(4)]))
      if it<=3 or it%10==0:emit({'iteration':it,'short_count':len(ws),'min_length':ws[0][0],'cuts':len(cut_masks),'seconds':time.time()-start})
    (ev/f'{label}_state.smt2').write_text(solver.to_smt2(),encoding='utf-8')
    (ev/f'{label}_last.json').write_text(json.dumps({'N':N,'m':m,'sequence':last,'cuts':len(cut_masks),'iterations':it},indent=2),encoding='utf-8')
    logfile.close()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--N',type=int,default=20);ap.add_argument('--m',type=int,default=14);ap.add_argument('--seconds',type=int,default=60);ap.add_argument('--affine',action='store_true');ap.add_argument('--bv',action='store_true');args=ap.parse_args()
    run(args.N,args.m,args.seconds,args.affine,args.bv)
