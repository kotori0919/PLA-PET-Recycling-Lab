# v0.8 전체 compliance

첨부 goal 0–25절의 디지털 gate다. 물리시험·안전인증이 아니다.

- `PASS` 00_authoritative_baseline: verified main/tag/handoff hashes
- `PASS` 02_v07_archive: archive index + classified manifest
- `FAIL` 03_calculix_core: LC02/04/05 + hot mount; source_current=False
- `PASS` 03_lc04_resolution: DIFFERENT_METRIC_OR_MODEL
- `FAIL` 03_hot_zone_mount: A–G=7 qualified={'scm440_temperature_dependent_material_qualified': False, 'sensor_bore_local_stress_qualified': True, 'die_joint_qualified': False, 'local_temperature_gradient_qualified': False} selected_SF=2.09 sensor_local_current=False sensor_thermal_pressure_screen=PASS/0.01634593636574816
- `PASS` 05_v08_motion_dynamics: v0.8 parameter-bound mechanical/control surrogate; source_current=True; not firmware/physical validation
- `FAIL` 05_loaded_phase_centre: source_current=False loaded=PASS key_source_current=True released_key_clocking=PASS candidate25_current=False candidate25=PASS/0.9036394083963866deg checks={'mesh_convergence': True, 'positive_loaded_backlash': True, 'backlash_below_one_degree': True, 'frame_and_bearing_compliance_qualified': True, 'torsional_phase_compliance_qualified': True}
- `PASS` 03_solver_qualification: torsion/thermal/modal + component screens; source_current=True; not complete assembly qualification
- `FAIL` 06_interface_catalog: single controlling rows=48; exhaustive_coverage=HOLD
- `FAIL` 06_tolerance_stacks: calculations/tolerance_stack_final.json
- `FAIL` 07_freecad_source: FreeCAD mount solids/collision/contact gate; source_current=False; axial_contact=PASS; candidate_current=False candidate=PASS/PASS
- `PASS` 08_step_package: rows=79 dirs=True files_current=True; file integrity only, not fabrication qualification
- `PASS` 09_print_package: rows=12 files_current=True; physical fit NOT_RUN
- `PASS` 10_manufacturing_package: cutter:PASS, shafts:PASS, phase_gears:PASS, screw_barrel:PASS, die:PASS, bearing_plates:PASS, feeder:PASS, hot_zone:PASS, guards_panels:PASS, RFQ:PASS
- `PASS` 11_dimensioned_drawings: rows=20 PDFs=20
- `PASS` 12_electrical_package: vector_diagrams=True wires=102
- `PASS` 13_firmware_release: source/binary/build/library/docs/reproducible build
- `PASS` 14_authoritative_bom: rows=119 digital=PASS procurement=HOLD
- `PASS` 15_assembly_manual: structured_steps=25 artifact_fields_and_pdfs=True execution_HOLD_steps=['7', '10', '12', '13']; completeness is separate from physical approval
- `PASS` 16_commissioning_handoff: transition_gates=6 physical=NOT_RUN
- `PASS` 17_multimodal_review: views=12 closeups=48 modules=6
- `PASS` 18_electrical_firmware_tests: state-machine + hardware-adapter
- `PASS` 19_independent_reviews: 12 required reviewer roles
- `FAIL` 20_release_package: deterministic ZIP schema/hash/clean-extraction verification
- `PASS` 21_release_policy: origin HEAD + open main-target PR verified; GitHub Release publish remains blocked

산출물 gate: **18/25**
원문 절 완료: **17/26**
전체 결과: **FAIL**

물리시험 `NOT_RUN` · 안전인증 `NOT_CERTIFIED` · 제작 승인 `USER_APPROVAL_REQUIRED`
