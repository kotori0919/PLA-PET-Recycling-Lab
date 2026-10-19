# v0.8 전체 compliance

첨부 goal 0–25절의 디지털 gate다. 물리시험·안전인증이 아니다.

- `PASS` 00_authoritative_baseline: verified main/tag/handoff hashes
- `PASS` 02_v07_archive: archive index + classified manifest
- `PASS` 03_calculix_core: LC02/04/05 + hot mount; source_current=True
- `PASS` 03_lc04_resolution: DIFFERENT_METRIC_OR_MODEL
- `PASS` 03_hot_zone_mount: A–G=7 qualified={'scm440_temperature_dependent_material_qualified': True, 'sensor_bore_local_stress_qualified': True, 'die_joint_qualified': True, 'local_temperature_gradient_qualified': True} selected_SF=2.089 sensor_local_current=True sensor_thermal_pressure_screen=PASS/0.01634593636574816
- `PASS` 05_v08_motion_dynamics: v0.8 parameter-bound mechanical/control surrogate; source_current=True; not firmware/physical validation
- `PASS` 05_loaded_phase_centre: source_current=True loaded=PASS key_source_current=True released_key_clocking=PASS candidate25_current=True candidate25=PASS/0.9036394083963866deg checks={'mesh_convergence': True, 'positive_loaded_backlash': True, 'backlash_below_one_degree': True, 'frame_and_bearing_compliance_qualified': True, 'torsional_phase_compliance_qualified': True}
- `PASS` 03_solver_qualification: torsion/thermal/modal + component screens; source_current=True; not complete assembly qualification
- `PASS` 06_interface_catalog: single controlling rows=48; exhaustive_coverage=PASS
- `PASS` 06_tolerance_stacks: calculations/tolerance_stack_final.json
- `PASS` 07_freecad_source: Integrated GGM frame={'status': 'FRAME_CUTLIST_BINDING_PASS', 'members': 40, 'totals': {'2020': {'count': 36, 'length_mm': 15078.0}, '2040': {'count': 4, 'length_mm': 2180.0}}, 'cut_authorization': False, 'stock_nesting_status': 'ACTUAL_STOCK_REQUIRED', 'frame_release_sha256': 'c411d44e1cb7cb934e6e40d8a37c22f7a4cf08e5ba0c062ca2101945f6b40747', 'cutlist_sha256': 'c1c1c2ac5372c2e059fb70991abbed6c07fc7c615a8dddcd96f73c2f21abece8'}; FreeCAD mount solids/collision/contact gate; source_current=True; axial_contact=PASS; candidate_current=True candidate=PASS/PASS
- `PASS` 08_step_package: rows=80 dirs=True files_current=True; file integrity only, not fabrication qualification
- `PASS` 09_print_package: rows=12 files_current=True; physical fit NOT_RUN
- `PASS` 10_manufacturing_package: cutter:PASS, shafts:PASS, phase_gears:PASS, screw_barrel:PASS, die:PASS, bearing_plates:PASS, feeder:PASS, hot_zone:PASS, guards_panels:PASS, drive_ggm:PASS, RFQ:PASS
- `PASS` 11_dimensioned_drawings: rows=20 PDFs=20
- `PASS` 12_electrical_package: vector_diagrams=True wires=101
- `PASS` 13_firmware_release: source/binary/build/library/docs/reproducible build
- `PASS` 14_authoritative_bom: rows=162 digital=PASS procurement=HOLD
- `PASS` 15_assembly_manual: structured_steps=25 artifact_fields_and_pdfs=True execution_HOLD_steps=['2', '7', '10', '12', '13']; completeness is separate from physical approval
- `PASS` 16_commissioning_handoff: transition_gates=6 physical=NOT_RUN
- `PASS` 17_multimodal_review: views=12 closeups=48 modules=6
- `PASS` 18_electrical_firmware_tests: state-machine + hardware-adapter
- `PASS` 19_independent_reviews: 12 required reviewer roles
- `FAIL` 20_release_package: deterministic ZIP schema/hash/clean-extraction verification
- `PASS` 21_release_policy: origin HEAD + open main-target PR verified; user-authorized prerelease only; physical approvals remain blocked

산출물 gate: **24/25**
원문 절 완료: **21/26**
전체 결과: **FAIL**

물리시험 `NOT_RUN` · 안전인증 `NOT_CERTIFIED` · 제작 승인 `USER_APPROVAL_REQUIRED`
