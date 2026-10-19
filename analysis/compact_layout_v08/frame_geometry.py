"""Export the two unchanged-member frames and real shelf load stations."""
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'cad/freecad/drive_v08')]
from analysis.compact_layout_v08.review import placement, by_name, CONTRACT
from analysis.frame_v08.audit_geometry import profiles, contacts, steel_tie
from cad.freecad.drive_v08.assembly import integrated_objects
from cad.freecad.final_v08.generate import final_objects
from validation.integrated_assembly_clearance import geometry_source_paths


def snapshot(items):
    by = by_name(items)
    rows = profiles(items)
    tie_spec = json.loads((ROOT/'cad/parameters/ggm_frame_revision.json').read_text())['tie']
    tie, section = steel_tie(tie_spec)
    b = tie.BoundBox
    rows.append({'id': tie_spec['object'], 'source_object': tie_spec['object'], 'axis': 0,
        'length_mm': b.XLength, 'box': [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],
        'section_properties': {'area_mm2': section.Area, 'iy_mm4': section.MatrixOfInertia.A22,
            'iz_mm4': section.MatrixOfInertia.A33, 'j_mm4': section.Area*tie_spec['thickness_mm']**2/3,
            'e_mpa': 200000.0, 'centroid_yz_mm': [section.CenterOfMass.y,section.CenterOfMass.z]}})
    rows = contacts(rows, items)
    stations = []
    for x in (90,220):
        for y, rail in ((100,'GGM_ShredRail'),(280,'MidRail500')):
            name = f'GGM_SH_Spacer_{x}_{y}'
            b = by[name].BoundBox
            stations.append({'id': name, 'rail': rail,
                'point_mm': [b.Center.x,b.Center.y,b.ZMin]})
    return {'members': rows, 'attachments': stations}


def main():
    paths = geometry_source_paths()+[CONTRACT,Path(__file__).resolve(),
        ROOT/'analysis/compact_layout_v08/review.py',ROOT/'analysis/frame_v08/audit_geometry.py']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    spec = json.loads(CONTRACT.read_text())
    before,_ = integrated_objects(final_objects(), compact_layout=False)
    after,_ = placement(before,tuple(spec['upper_translation_mm']),
        tuple(spec['support_and_collection_translation_mm']))
    result = {'before':snapshot(before),'after':snapshot(after),'source_sha256':hashes,
        'status':'COMPACT_FRAME_INPUT_EXPORTED','canonical_geometry_promoted':False,
        'physical_validation_state':'NOT_RUN','fabrication_authorized':False}
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h for p,h in hashes.items()):
        raise ValueError('source changed during export')
    out=Path(__file__).parent/'results/frame_geometry.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(result['status'], 'members',len(result['after']['members']),
          'attachments',result['after']['attachments'],flush=True)


if __name__=='__main__': main()
