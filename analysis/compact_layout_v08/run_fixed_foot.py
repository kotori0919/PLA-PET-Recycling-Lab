"""Export a compact layout with unchanged rail and four-foot locations."""
import hashlib
import json
from pathlib import Path
import sys
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'cad/freecad/drive_v08')]
from analysis.compact_layout_v08.fixed_foot_layout import candidate,validate
from analysis.compact_layout_v08.frame_geometry import snapshot
from analysis.compact_layout_v08.review import by_name,compare_solids
from validation.integrated_assembly_clearance import audit,geometry_source_paths
from cad.freecad.final_v08.generate import final_objects
from cad.freecad.drive_v08.assembly import integrated_objects
from cad.freecad.compact.generate import normalize_step,normalize_zip_container


def main():
    base,_=integrated_objects(final_objects(), compact_layout=False); rows,transforms,holes=candidate(base)
    result=validate(base,rows,transforms,holes); result['static']=audit(rows)
    source_paths=geometry_source_paths()+[ROOT/'analysis/compact_layout_v08'/name for name in
        ('run_fixed_foot.py','fixed_foot_layout.py','frame_geometry.py','review.py','contract.json')]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    out=ROOT/'exports/review/compact_layout_v08/fixed_foot';out.mkdir(parents=True,exist_ok=True)
    compound=Part.makeCompound([r['shape'] for r in rows]); path=out/'PPR-FIXED-FOOT-REVIEW.step'
    compound.exportStep(str(path));normalize_step(path)
    imported=Part.read(str(path))
    if not imported.isValid(): raise ValueError('invalid STEP')
    result['step_equivalence']=compare_solids(compound.Solids,imported.Solids)
    doc=App.newDocument('PPRFixedFootReview')
    for row in rows:
        ob=doc.addObject('PartDesign::Feature',row['name']);ob.Shape=row['shape'];ob.Label=row['name']
    doc.recompute();native=out/'PPR-FIXED-FOOT-REVIEW.FCStd'
    native.unlink(missing_ok=True);doc.saveAs(str(native));App.closeDocument(doc.Name)
    normalize_zip_container(native,normalize_fcstd=True)
    plates=[]
    for label,items in (('before',base),('after',rows)):
        plate=by_name(items)['GGM_SH_Base'];step=out/f'SHELF-{label}.step'
        plate.exportStep(str(step));normalize_step(step)
        plates.append({'variant':label,'step':str(step.relative_to(ROOT)),
            'sha256':hashlib.sha256(step.read_bytes()).hexdigest()})
    frame={'before':snapshot(base),'after':snapshot(rows),'source_sha256':hashes,
        'status':'FIXED_FOOT_FRAME_INPUT_EXPORTED','physical_validation_state':'NOT_RUN'}
    result.update(status='FIXED_FOOT_LAYOUT_GEOMETRY_PASS',source_sha256=hashes,
        frame_inputs=frame,shelf_inputs=plates,physical_validation_state='NOT_RUN',
        fabrication_authorized=False,energization_authorized=False,canonical_geometry_promoted=False,
        modified_part='GGM_SH_Base: relocate four existing foot holes; unchanged stock and post holes',
        step=str(path.relative_to(ROOT)),step_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        native=str(native.relative_to(ROOT)),native_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
        limitations=['Shelf plate and four-foot reaction distribution must be checked before canonical adoption.',
            'This file does not certify joints, actual hardware, thermal performance or commissioning.'])
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h for p,h in hashes.items()):
        raise ValueError('source changed during export')
    result_path=Path(__file__).parent/'results/fixed_foot_geometry.json'
    result_path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(result['status'],result['dimensions_mm'],result['step_equivalence'],flush=True)

if __name__=='__main__': main()
