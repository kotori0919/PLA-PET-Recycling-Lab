"""Move the upper module but keep frame rails and four shelf feet in place."""
import json
import FreeCAD as App
import Part
from analysis.compact_layout_v08.review import placement, by_name


def candidate(base):
    rows,transforms=placement(base)
    original=by_name(base); fixed={'MidRail500','GGM_ShredRail'}
    fixed.update(n for n in original if n.startswith('GGM_SH_Spacer_'))
    for row in rows:
        if row['name'] in fixed:
            row['shape']=original[row['name']].copy()
            transforms.pop(row['name'],None)
    by=by_name(rows); stock_box=by['GGM_SH_Base'].BoundBox
    plate=Part.makeBox(stock_box.XLength,stock_box.YLength,stock_box.ZLength,
        App.Vector(stock_box.XMin,stock_box.YMin,stock_box.ZMin))
    holes=[]
    for name,shape in by.items():
        if name.startswith('GGM_SH_Spacer_'): diameter=6.6
        elif name.startswith('GGM_SH_Post_'): diameter=5.5
        else: continue
        b=shape.BoundBox; x,y=b.Center.x,b.Center.y
        margin=min(x-stock_box.XMin,stock_box.XMax-x,y-stock_box.YMin,stock_box.YMax-y)-diameter/2
        if margin<5: raise ValueError('insufficient existing plate hole edge ligament: '+name)
        hole=Part.makeCylinder(diameter/2,stock_box.ZLength,App.Vector(x,y,stock_box.ZMin))
        plate=plate.cut(hole); holes.append({'mating_object':name,'x_mm':x,'y_mm':y,'diameter_mm':diameter})
    if len(holes)!=8 or not plate.isValid() or len(plate.Solids)!=1:
        raise ValueError('invalid eight-hole support plate')
    for row in rows:
        if row['name']=='GGM_SH_Base': row['shape']=plate.removeSplitter()
    if abs(plate.Volume-original['GGM_SH_Base'].Volume)>0.01:
        raise ValueError('new material or hole-volume drift')
    return rows,transforms,holes


def validate(base,rows,transforms,holes):
    from analysis.compact_layout_v08 import review as r
    before,after=by_name(base),by_name(rows)
    if set(before)!=set(after): raise ValueError('component addition or omission')
    for row in rows:
        name=row['name']
        if name=='GGM_SH_Base': continue
        target=before[name].copy();target.translate(App.Vector(*transforms.get(name,(0,0,0))))
        if max(target.cut(after[name]).Volume,after[name].cut(target).Volume)>0.01:
            raise ValueError('unrequested geometry change: '+name)
    result={'dimensions_mm':r.dimensions(rows),'supports':r.check_supports(base,rows),
        'collection':r.check_collection(rows),'lid':r.check_lid(rows,json.loads(r.CONTRACT.read_text())),
        'lower_motion':r.check_lower_motion(rows),'hole_schedule':holes}
    if any(abs(a-b)>1e-5 for a,b in zip(result['dimensions_mm'],(470,700,930))):
        raise ValueError('compact envelope drift')
    for hole in holes:
        shape=after[hole['mating_object']];b=shape.BoundBox
        if max(abs(b.Center.x-hole['x_mm']),abs(b.Center.y-hole['y_mm']))>1e-6:
            raise ValueError('hole/mating axis drift')
        pb=after['GGM_SH_Base'].BoundBox
        probe=Part.makeCylinder(hole['diameter_mm']/2-0.005,pb.ZLength,App.Vector(hole['x_mm'],hole['y_mm'],pb.ZMin))
        if after['GGM_SH_Base'].common(probe).Volume>0.01:
            raise ValueError('required mounting hole missing: '+hole['mating_object'])
        previous=r.contact_area(before['GGM_SH_Base'],before[hole['mating_object']])
        present=r.contact_area(after['GGM_SH_Base'],shape)
        if previous<1 or present<previous-0.01:
            raise ValueError('plate mating face lost: '+hole['mating_object'])
    return result
