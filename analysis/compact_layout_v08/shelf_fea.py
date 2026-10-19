"""Local shelf stiffness screen for relocation; bolt/contact approval is separate."""
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/final_validation')]
from analysis.final_validation.run_calculix_v08 import nset,solve,printed_reactions
from analysis.radial_support_v08.plate_fea import equilibrium
from analysis.compact_layout_v08.quadratic_mesh import mesh_step,read_gmsh_inp,exterior_faces


def deck(nodes,elements,variant,direction):
    dx,dy=(0.,0.) if variant=='before' else (-18.,29.)
    feet=[(x,y) for x in (90.,220.) for y in (100.,280.)]
    posts=[(x+dx,y+dy) for x in (55.,248.) for y in (233.,293.)]
    fixed=[n for n,(x,y,z) in nodes.items()
           if min(abs(math.hypot(x-a,y-b)-3.3) for a,b in feet)<0.06]
    weights=[defaultdict(float) for _ in posts]
    for face in exterior_faces(elements):
        pts=np.asarray([nodes[n] for n in face])
        if max(abs(pts[:,2]-536.))>1e-5: continue
        area=float(np.linalg.norm(np.cross(pts[1]-pts[0],pts[2]-pts[0])))/2
        for index,(x,y) in enumerate(posts):
            centre=pts.mean(axis=0)
            if abs(centre[0]-x)<=10 and abs(centre[1]-y)<=10:
                for n in face[3:]: weights[index][n]+=area/3
    if direction not in (-1,1) or len(fixed)<12 or any(len(w)<3 for w in weights):
        raise ValueError('insufficient shelf fixing or post patch mesh')
    forces=defaultdict(float)
    for patch in weights:
        for n,w in patch.items(): forces[n]+=direction*100.*w/sum(patch.values())
    xyz={n:tuple(v/1000 for v in p) for n,p in nodes.items()}
    applied={'force_n':[0.,0.,sum(forces.values())],
        'moment_nm':sum((np.cross(xyz[n],[0.,0.,f]) for n,f in forces.items()),np.zeros(3)).tolist(),
        'post_patch_areas_mm2':[sum(w.values()) for w in weights],
        'load_basis':'100 N per post, four posts; numerical unit-load comparison, not an established machine load'}
    lines=['*HEADING','PPR shelf plate delta, SI units', '*NODE',
        *(f'{n},{x:.12g},{y:.12g},{z:.12g}' for n,(x,y,z) in xyz.items()),
        '*ELEMENT,TYPE=C3D10,ELSET=ALL',*elements,*nset('REACTION',fixed),
        '*SOLID SECTION,ELSET=ALL,MATERIAL=STEEL','', '*MATERIAL,NAME=STEEL',
        '*ELASTIC','200000000000.,0.3','*BOUNDARY','REACTION,1,3,0',
        '*STEP','*STATIC','0.1,1.0','*CLOAD',*(f'{n},3,{f:.12g}' for n,f in forces.items()),
        '*NODE PRINT,NSET=REACTION','RF','*NODE FILE','U,RF','*EL FILE','S','*END STEP','']
    return '\n'.join(lines),applied,{n:xyz[n] for n in fixed}


def main():
    root=Path(__file__).parent; gp=root/'results/fixed_foot_geometry.json'
    geometry=json.loads(gp.read_text()); hashes=dict(geometry['source_sha256'])
    for p in (Path(__file__).resolve(),gp,ROOT/'analysis/final_validation/run_calculix_v08.py',
              ROOT/'analysis/structural/run_load_checks.py',ROOT/'analysis/radial_support_v08/plate_fea.py',
              ROOT/'analysis/compact_layout_v08/quadratic_mesh.py'):
        hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    if not all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items()):
        raise ValueError('stale shelf geometry inputs')
    out=ROOT/'.build/compact-purpose-continue-20260915/shelf-raw';out.mkdir(exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='run-',dir=out)); rows=[]
    for item in geometry['shelf_inputs']:
        step=ROOT/item['step']; variant=item['variant']
        if hashlib.sha256(step.read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('shelf STEP hash mismatch')
        hashes[item['step']]=item['sha256']
        for size in (6.,4.,2.):
            mesh_folder=folder/f'{variant}-{size:g}';mesh_folder.mkdir()
            mesh=mesh_step(step,mesh_folder,size);nodes,elements=read_gmsh_inp(mesh)
            for direction in (-1,1):
                case=mesh_folder/f'load-{direction}';case.mkdir()
                text,applied,coords=deck(nodes,elements,variant,direction)
                result=solve(case,text); reaction=printed_reactions(case/'model.dat',coords)
                balance=equilibrium(applied,reaction)
                row={'variant':variant,'mesh_mm':size,'direction':direction,
                    'nodes':len(nodes),'elements':len(elements),'applied':applied,
                    'result':result,'equilibrium':balance,'raw_dir':str(case.relative_to(ROOT)),
                    'raw_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                        (case/'model.inp',case/'model.dat',case/'model.frd',case/'ccx.log')}}
                rows.append(row)
                print('SHELF_CASE',variant,size,direction,result,balance,flush=True)
    refinement=[]
    for variant,direction in ((v,d) for v in ('before','after') for d in (-1,1)):
        selected=[r for r in rows if r['variant']==variant and r['direction']==direction]
        medium,fine=selected[-2:]
        a,b=(r['result']['max_displacement_mm'] for r in (medium,fine))
        refinement.append({'variant':variant,'direction':direction,
            'displacement_relative_change':abs(a-b)/b,'converged':abs(a-b)/b<=0.05})
    checks={'twelve_cases':len(rows)==12,'all_equilibrium':all(r['equilibrium']['passed'] for r in rows),
        'all_solver_pass':all(r['result']['status']=='PASS' for r in rows),
        'displacement_convergence':all(r['converged'] for r in refinement)}
    checks['sources_unchanged']=all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
    report={'status':'SHELF_NUMERICAL_COMPARISON_PASS' if all(checks.values()) else 'FAIL',
        'checks':checks,'cases':rows,'refinement':refinement,'source_sha256':hashes,
        'physical_validation_state':'NOT_RUN','fabrication_authorized':False,
        'canonical_geometry_promoted':False,'strength_qualified':False,
        'limitations':['C3D10 linear elastic, ideal fixed bolt bores; no bolt preload, slip or spacer contact.',
            'Four 100 N post loads are comparison excitations, not measured working loads or a qualified proof load.',
            'Sharp-hole and fixed-boundary peak stresses are reported, not used as an accepted strength value.',
            'Shelf, posts, joints, and frame are not solved as one nonlinear assembly.']}
    path=root/'results/shelf_fea.json';path.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(report['status'],checks,flush=True)
    if not all(checks.values()): raise SystemExit(2)


if __name__=='__main__': main()
