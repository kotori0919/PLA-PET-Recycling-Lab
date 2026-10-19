# PPR-C10 — Traverse carriage

- revision: `safety-orchestration-closure-v0.6.1`
- quantity: 1
- material: PLA
- nozzle diameter: 0.4 mm
- orientation: flat
- layer height: 0.20 mm
- wall count: 5
- top/bottom layers: 5
- infill: 40%
- support: rod bores only
- support-contact region: two Ø8.4 rod-bores
- support removal: ream rod bores to Ø8.40–8.50 and belt-clamp holes to Ø4.50–4.70
- brim: none
- designed minimum wall: 2.0 mm
- estimated mass: 89.2 g/ea, 89.2 g total
- estimated print time: 7.4 h at 12 g/h planning rate
- fastener: 2x M4x25 belt-clamp screws + washers + nyloc
- insert or captured nut: none
- tightening torque: 1.2 N.m
- fastener edge distance: 8 mm from belt-pad edge
- physical interfaces: 2x Ø8.40–8.50 rod bores; 2x Ø4.50–4.70 through clamp bores
- tolerance: finished rod bores Ø8.40–8.50; finished clamp holes Ø4.50–4.70; use two Ø8 h6=7.991–8.000 ground steel rods
- mating part: specified Ø8 h6 rods and GT2 belt
- assembly order: 19
- bounding box: 90.0 x 55.0 x 24.0 mm
- FreeCAD Python source: `PPR-C10.py` -> `cad/freecad/compact/geometry.py`
- dimension sheet: `dimension_sheet.svg`

Slicer 질량·시간은 `print_manifest.csv`와 `total_material_report.md`의 PrusaSlicer 결과가 지배한다.

<!-- SLICER_EVIDENCE_BEGIN -->
- PrusaSlicer package mass: **63.26 g** for released quantity
- PrusaSlicer package time: **4.81 h**
- support extrusion volume: **4.735 cm³** (G-code role integration; included in package mass)
<!-- SLICER_EVIDENCE_END -->
