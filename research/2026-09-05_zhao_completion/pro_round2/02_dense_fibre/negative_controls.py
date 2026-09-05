"""Reject deliberately corrupted inputs. These failed checks are expected tests,
not unresolved branches of the theorem."""
import sys
if sys.flags.optimize: raise RuntimeError('Run without -O.')
from pathlib import Path
import importlib.util,tempfile,json,shutil
ROOT=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/f'{name}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def rejects(action):
    try:action()
    except (AssertionError,ValueError,RuntimeError):return True
    return False

farkas=load('verify_farkas');roots=load('verify_roots')
results=[]
with tempfile.TemporaryDirectory(prefix='sf2_negative_') as d:
    p=Path(d)
    original=json.loads((ROOT/'farkas_certificate.json').read_text())
    for key in ('rhs','unknown_zero_layer'):
        c=json.loads(json.dumps(original))
        if key=='rhs':c['right_hand_side']+=1
        else:c['multipliers'][14]=1
        (p/'farkas_certificate.json').write_text(json.dumps(c))
        ok=rejects(lambda:farkas.validate(p));assert ok;results.append({'mutation':key,'rejected':ok})
    lines=(ROOT/'rank3_roots.txt').read_text().splitlines()
    for key,mutated in (('one_root_omitted',lines[:-1]),('one_root_duplicated',lines[:-1]+[lines[0]])):
        (p/'rank3_roots.txt').write_text('\n'.join(mutated)+'\n')
        ok=rejects(lambda:roots.validate(p));assert ok;results.append({'mutation':key,'rejected':ok})
print(json.dumps({'negative_controls_total':4,'rejected':4,'tests':results,'exit':'NORMAL'},indent=2))
