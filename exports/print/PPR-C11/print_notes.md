# PPR-C11 — Control panel bezel

- revision: `safety-orchestration-closure-v0.6.1`
- quantity: 1
- material: PLA
- nozzle diameter: 0.4 mm
- orientation: front face down
- layer height: 0.20 mm
- wall count: 4
- top/bottom layers: 4
- infill: 20%
- support: no
- support-contact region: none
- support removal: ream fastener holes to Ø3.40–3.50
- brim: none
- designed minimum wall: 1.6 mm
- estimated mass: 61.5 g/ea, 61.5 g total
- estimated print time: 5.1 h at 12 g/h planning rate
- fastener: 4x M3x16 + washers + all-metal nuts
- insert or captured nut: none
- tightening torque: 0.5 N.m
- fastener edge distance: 8 mm boss centre; Ø12 boss
- physical interfaces: 4x Ø3.40–3.50 through bores; 145x82 display opening
- tolerance: finished holes Ø3.40–3.50; 0.25 mm TFT
- mating part: metal control panel
- assembly order: 21
- bounding box: 180.0 x 120.0 x 8.0 mm
- FreeCAD Python source: `PPR-C11.py` -> `cad/freecad/compact/geometry.py`
- dimension sheet: `dimension_sheet.svg`

Slicer 질량·시간은 `print_manifest.csv`와 `total_material_report.md`의 PrusaSlicer 결과가 지배한다.

<!-- SLICER_EVIDENCE_BEGIN -->
- PrusaSlicer package mass: **43.63 g** for released quantity
- PrusaSlicer package time: **4.06 h**
- support extrusion volume: **0.000 cm³** (G-code role integration; included in package mass)
<!-- SLICER_EVIDENCE_END -->
