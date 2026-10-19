"""Review-only inset layout with the front crossrail held at its original datum."""
from pathlib import Path
import json
import sys
import FreeCAD as App
import Part
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.compact_layout_v08.review import placement, by_name, CONTRACT


def proposal(base):
    spec = json.loads(CONTRACT.read_text())
    upper = tuple(spec['upper_translation_mm'])
    support = tuple(spec['support_and_collection_translation_mm'])
    candidate, transforms = placement(base, upper, support)
    old, new = by_name(base), by_name(candidate)
    front_spacers = ['GGM_SH_Spacer_90_100', 'GGM_SH_Spacer_220_100']
    plate = new['GGM_SH_Base']
    z, depth = plate.BoundBox.ZMin, plate.BoundBox.ZLength
    if abs(depth-6.0)>1e-6:
        raise ValueError('unexpected base plate thickness')
    old_holes, new_holes = [], []
    for name in front_spacers:
        b = new[name].BoundBox
        old_holes.append(Part.makeCylinder(3.3,depth,App.Vector(b.Center.x,b.Center.y,z)))
        original = old[name].BoundBox
        new_holes.append(Part.makeCylinder(3.3,depth,App.Vector(original.Center.x+upper[0],original.Center.y,z)))
    for hole in old_holes:
        if plate.common(hole).Volume > 0.01:
            raise ValueError('reference mounting hole not empty')
        plate = plate.fuse(hole)
    for hole in new_holes:
        if abs(plate.common(hole).Volume-hole.Volume)>0.01:
            raise ValueError('new mounting hole is not inside solid plate')
        plate = plate.cut(hole)
    plate = plate.removeSplitter()
    if not plate.isValid() or len(plate.Solids)!=1:
        raise ValueError('invalid revised mounting plate')
    for row in candidate:
        name = row['name']
        if name == 'GGM_SH_Base':
            row['shape'] = plate
            row['material'] += '; review: front M6 mounting row retains Y100 datum'
        elif name == 'GGM_ShredRail':
            row['shape'] = old[name].copy(); transforms[name] = [0,0,0]
        elif name in front_spacers:
            row['shape'] = old[name].copy()
            row['shape'].translate(App.Vector(upper[0],0,0))
            transforms[name] = [upper[0],0,0]
    return candidate, transforms


def check_mounts(base, candidate):
    from analysis.compact_layout_v08.review import check_supports
    from validation.integrated_motion_clearance import contact_area
    by = by_name(candidate)
    contacts = check_supports(base, candidate)
    plate = by['GGM_SH_Base']
    for x in (90,220):
        for y in (100,280):
            name = f'GGM_SH_Spacer_{x}_{y}'
            spacer = by[name]; b = spacer.BoundBox
            face = contact_area(plate, spacer)
            if face < 70.0:
                raise ValueError('spacer does not seat under plate: '+name)
            bore = Part.makeCylinder(3.3, plate.BoundBox.ZLength,
                App.Vector(b.Center.x,b.Center.y,plate.BoundBox.ZMin))
            if plate.common(bore).Volume > 0.01:
                raise ValueError('base bolt hole not aligned: '+name)
            contacts[name+'/GGM_SH_Base'] = {'after_mm2': face}
    return contacts


def main():
    import hashlib
    from cad.freecad.final_v08.generate import final_objects
    from cad.freecad.drive_v08.assembly import integrated_objects
    from cad.freecad.compact.generate import normalize_step
    from analysis.compact_layout_v08 import review as r
    paths = r.geometry_source_paths()+[Path(__file__).resolve(), r.CONTRACT,
        ROOT/'analysis/compact_layout_v08/review.py',
        ROOT/'validation/integrated_assembly_clearance.py',
        ROOT/'validation/integrated_motion_clearance.py']
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    source = {str(p.relative_to(ROOT)):sha(p) for p in paths}
    base, _ = integrated_objects(final_objects(), compact_layout=False)
    candidate, transforms = proposal(base)
    r.check_preserved([v for v in base if v['name']!='GGM_SH_Base'],
                      [v for v in candidate if v['name']!='GGM_SH_Base'], transforms)
    static = r.audit(candidate)
    supports = check_mounts(base,candidate)
    collection = r.check_collection(candidate)
    lower = r.check_lower_motion(candidate)
    envelope = r.dimensions(candidate)
    if any(abs(v-t)>1e-5 for v,t in zip(envelope,(470,700,930))):
        raise ValueError('review envelope changed')
    folder = ROOT/'exports/review/compact_layout_v08/support_datum'
    folder.mkdir(parents=True,exist_ok=True)
    compound = Part.makeCompound([v['shape'] for v in candidate])
    step = folder/'PPR-COMPACT-SUPPORT-REVIEW.step'
    compound.exportStep(str(step)); normalize_step(step)
    roundtrip = r.compare_solids(compound.Solids,Part.read(str(step)).Solids)
    plate_file = folder/'GGM_SH_Base.step'
    by_name(candidate)['GGM_SH_Base'].exportStep(str(plate_file)); normalize_step(plate_file)
    result = {'status':'COMPACT_SUPPORT_DATUM_REVIEW_PASS', 'envelope_mm':envelope,
        'static':static,'supports':supports,'collection':collection,'lower_motion':lower,
        'step_equivalence':roundtrip,'source_sha256':source,
        'artifacts_sha256':{str(p.relative_to(ROOT)):sha(p) for p in (step,plate_file)},
        'physical_validation_state':'NOT_RUN','fabrication_authorized':False,
        'canonical_geometry_promoted':False,
        'remaining_digital_work':['Local base plate stiffness with changed mount row',
            'Lid rail/latch/interlock design','Canonical integration and affected source regeneration']}
    if any(sha(ROOT/p)!=h for p,h in source.items()):
        raise ValueError('source changed during support review')
    output=Path(__file__).with_name('results')/'support_datum.json'
    output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(result['status'],'envelope',envelope,'contacts',len(supports),flush=True)

if __name__=='__main__': main()
