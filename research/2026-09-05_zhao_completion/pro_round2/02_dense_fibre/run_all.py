#!/usr/bin/env python3
"""Reproduce all finite certificates, with no search time/node/pool cutoff.
Requires Python 3 and a C++17 compiler with OpenMP (default: g++).
All generated files go into a fresh output directory; supplied evidence is not overwritten.
"""
from __future__ import annotations
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'replay')
    p.add_argument('--threads',type=int,default=4)
    p.add_argument('--compiler',default='g++')
    args=p.parse_args()
    if args.threads<1:p.error('--threads must be positive')
    if sys.flags.optimize:p.error('Do not use Python -O.')
    output=args.output.resolve()
    if output.exists() and any(output.iterdir()):p.error('Output directory must be absent or empty.')
    output.mkdir(parents=True,exist_ok=True)
    compiler=shutil.which(args.compiler)
    if compiler is None:raise RuntimeError(f'C++ compiler not found: {args.compiler}')
    records=[];started=time.monotonic()
    report={'python':sys.version,'platform':platform.platform(),'machine':platform.machine(),
            'compiler':subprocess.check_output([compiler,'--version'],text=True),
            'threads':args.threads,'source_sha256':{x.name:digest(x) for x in sorted(ROOT.iterdir()) if x.suffix in ('.cpp','.py') or x.name in ('rank3_roots.txt','farkas_certificate.json')},'commands':records}
    def run(name:str,command:list[str])->None:
        tick=time.monotonic()
        with (output/f'{name}.log').open('w') as stdout,(output/f'{name}.err').open('w') as stderr:
            result=subprocess.run(command,cwd=ROOT,stdout=stdout,stderr=stderr,check=False)
        (output/f'{name}.exit').write_text(str(result.returncode)+'\n')
        records.append({'name':name,'argv':command,'returncode':result.returncode,'seconds':time.monotonic()-tick})
        (output/'execution_report.json').write_text(json.dumps(report,indent=2)+'\n')
        if result.returncode!=0:raise RuntimeError(f'{name} exited {result.returncode}; inspect its logs.')
    try:
        for name in ('generate_roots','search_reference','verify_extensions','unit_search_reference','unit_verify_extensions'):
            flags=['-O3','-std=c++17','-Wall','-Wextra','-Werror','-Wno-misleading-indentation']
            if name in ('verify_extensions','unit_verify_extensions'):flags+=['-fopenmp']
            run('build_'+name,[compiler,*flags,str(ROOT/f'{name}.cpp'),'-o',str(output/name)])
        run('generate_roots',[str(output/'generate_roots'),str(output/'rank3_roots.regenerated.txt')])
        if (output/'rank3_roots.regenerated.txt').read_bytes()!=(ROOT/'rank3_roots.txt').read_bytes():raise RuntimeError('Regenerated roots differ.')
        for name in ('verify_roots','verify_farkas','audit_interfaces','audit_legacy_models','negative_controls'):
            run(name,[sys.executable,'-I',str(ROOT/f'{name}.py')])
        for name in ('unit_search_reference','unit_verify_extensions'):
            run(name,[str(output/name)])
        run('search_reference',[str(output/'search_reference'),str(ROOT/'rank3_roots.txt')])
        run('verify_extensions',[str(output/'verify_extensions'),str(ROOT/'rank3_roots.txt'),str(args.threads)])
        run('verify_logs',[sys.executable,'-I',str(ROOT/'verify_logs.py'),'--source',str(ROOT),'--logs',str(output)])
        report.update({'exit':'NORMAL','elapsed_seconds':time.monotonic()-started,'all_commands_exit_zero':all(r['returncode']==0 for r in records)})
        (output/'execution_report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'exit':'NORMAL','output':str(output),'commands':len(records),'all_commands_exit_zero':True},indent=2))
        return 0
    except BaseException as exc:
        report.update({'exit':'ABNORMAL','error':repr(exc),'elapsed_seconds':time.monotonic()-started})
        (output/'execution_report.json').write_text(json.dumps(report,indent=2)+'\n')
        raise

if __name__=='__main__':raise SystemExit(main())
