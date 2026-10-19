# v0.8 현재 closure 보고서

report_state: `CURRENT` · 전체 gate: `IN_PROGRESS` · 제작: `HOLD`

## source baseline and final commit

- 기준 main: `7de9bf2a6e4c91c7fa6b58da9c729e63dc52e3a0`
- 현재 branch/HEAD: `final-design-fabrication-closure-v0.8` / `bf30b90e765668be1212ff8c383ff6b4d99276a1`
- final commit: `NOT_ESTABLISHED—미해결 gate와 작업트리 변경 존재`

## design changes and reasons / architecture drift

- v0.8은 hot-zone 지지, 하중 위상, 공차·인터페이스 및 패키지 증거를 재검증하도록 재개됐다.
- architecture: `compact_single_path`; scope decision=`NOT_COMPLETED_BY_SCOPE_DECISION`.
- architecture drift: `NONE_DETECTED`; 200 g/h는 release 기준이 아닌 stretch target이다.

## LC04 resolution / hot-zone mount resolution / final safety factors

- LC04 resolution: `DIFFERENT_METRIC_OR_MODEL`; fine displacement=0.0011791710270408191 mm.
- hot-zone mount resolution: `PASS`; selected=`C_RADIAL_CONTROLLED_AXIAL_EXPANSION`; selected safety factor=2.089.
- qualification gaps: `{'scm440_temperature_dependent_material_qualified': True, 'sensor_bore_local_stress_qualified': True, 'die_joint_qualified': True, 'local_temperature_gradient_qualified': True}`. 위 safety factor는 디지털 선형 모델이며 실제 재료·접촉·시험 인증이 아니다.
- sensor-bore conditional thermal-pressure screen: `PASS`; fine peak=49.934606554121274 MPa; conditional SF=3.5546490149595527; source_current=True.

## final dimensions and mass / part count

- assembly envelope: `[470.0, 729.0, 930.0]` mm; active CAD body count=266.
- final machine mass: `NOT_ESTABLISHED`—donor 실물과 혼합 소재 질량이 확정되지 않았다.
- BOM line count=162; scheduled quantity sum=246 (질량이나 고유 부품 수가 아님).

## print mass and time / STEP STL 3MF count / drawing count

- print mass=921.44 g; estimated print time=297299 s (82.58 h); physical print/fit=`NOT_RUN`.
- STEP count=80; STL count=12; 3MF count=12; drawing count=20.

## BOM / firmware / manual PDF

- BOM: 162 lines, digital integrity PASS, procurement HOLD.
- firmware build hash: `9e1f0b0f69aa2759948349f4b40e0e2ac1f4cc74eec2b31dbfcf2d349fc5db22`; physical I/O commissioning NOT_RUN.
- manual/PDF count=15 (manual 6 + commissioning/validation 9).

## release ZIP hash / known limitations

- release ZIP hash: `NOT_CREATED; 기존 파일은 과거 산출물 SHA-256 ce91530bf56a9ea26b0d3e13ecc5ff54899fbb1ba9d1d60ed4e9efef1ebb7955`.
- known limitations: `20_release_package`.
- cutter key clocking: current-source=`True`, released left/right check=`PASS`; actual optical/CMM inspection remains NOT_RUN.
- 25 mm phase-path candidate: current-source=`True`, numeric angle=`PASS`, total=`0.9036394083963866` deg, solid18 mm/34 N·m gear elastic=`0.03766627298193966` deg, conditional strength=`PASS`/SF `2.235495628771114`/stress convergence `0.02449477349851453`, state=`PASS`; 이는 범위가 제한된 디지털 증거다. 활성 CAD 반영 여부는 현재 파라미터와 assembly manifest로 확인하며, 전체 release 적격성과 실물 fit은 별도 gate다.
- rear axial retainer candidate: current-source=`True`, numeric=`PASS`, bolt proof SF=`4.103112391410234`, thread pullout SF=`2.4524757431063753`, minimum preload/load=`2.25605111459207`, state=`PASS`; 이 값만으로 최종 체결부 적격성을 승인하지 않는다. 활성 CAD 반영 여부와 고온 재료·예압/접촉 가정, 실물 마찰·열이완은 각각의 gate에서 구분한다.
- extruder thrust stack: NSK 51102 dynamic SF=`8.549939344970946`, static SF=`13.550847263727537`, Ruland MCLX-12-12-F torque SF=`7.753572273816298`, state=`PASS`. Ø15 h6 seat·Ø23 받침·Ø28.30–28.35 pocket·금속 shim 계약으로 IF-020은 디지털 PASS이며 수령/endplay/추력 proof는 NOT_RUN이다. IF-008은 GMP60 수령 한계가 포함된 디지털 기준 변형만 PASS이고 구매·수령·Gate-1은 HOLD다.
- tolerance blockers: numeric FAIL=[]; NOT_EVALUATED=[]; assumption-bound=[]. PASS 수치라도 blockers가 있으면 release PASS가 아니다.
- physical validation prerequisites: donor 라벨·정격·치수 확인, lockout, PE/퓨즈/interlock 검사, 단계별 사용자 승인과 실제 시험.
- user decisions still required: Tempco 승인도면·견적 검토, donor 선정, JLCCNC를 제외한 SCM440/QT/질화 전문 공급업체 선정, 구매·가공·통전·시운전 승인.

## 사용자 지정 조달 경로 조사 (2026-09-08)

- JLCCNC의2026-09-08 서면 회신은 비목록 SCM440 조달, Q&T, 가스질화와 그 최종
  물성·경도·층깊이 보증을 지원하지 않으며, 일반 최저 공차는±0.05 mm이고 개별
  형상·검사는 STEP/CNC Remark 업로드 후 심사한다고 답했다. 같은 주문에서 coupon을
  먼저 제작·승인한 뒤 본품을 진행하는 순서도 지원하지 않는다. 따라서 JLCCNC는
  현 EX-SCR-01/EX-BAR-01 사양의 일괄 공급처에서 `REJECTED_FOR_CURRENT_SPEC`이며,
  전문 SCM440/QT/질화/후가공 업체 선정 전 발주 금지를 유지한다.
  증적: docs/final/jlccnc_response_2026-09-08_ko.md
- T1–T4 기준품은 Tempco MTA1 맞춤 K형 비접지 MI probe다. 계약은 Alloy600,
  Ø3.00±0.03 mm, 25.40±0.25 mm sheath, 공급자 용접 Ø6.00±0.05×0.80±0.05 mm
  stop collar, 배럴 collar-to-tip5.20±0.05 mm 및 다이10.00±0.05 mm다.
  TH-TCR-01 bridge/SYS-17 체결과 보어 공차를 RFQ·BOM·FreeCAD 원본에 반영했다.
  제조사 승인도면·견적과 수령 후 치수/절연/교정/열응답/pull 시험 전에는
  `QUOTE_AND_RECEIPT_HOLD`이며 구매 승인이나 실물 검증 완료가 아니다.
  근거: docs/final/thermocouple_selection_basis_ko.md
- M8 spring/compression형 제품 ID `1005004962533904`는 나사 포트가 없는 현행 blind bore와
  직접 호환된다는 증거가 없어 채택하지 않았다. 배럴을 M8로 재가공하지 않는다.

## branch/PR/release state

- branch: `final-design-fabrication-closure-v0.8`; PR: `https://github.com/kotori0919/PLA-PET-Recycling-Lab/pull/4` / `OPEN`.
- GitHub publication: `PRERELEASE_AUTHORIZED`; actual published state is observed from the GitHub Release API; fabrication approval: `USER_APPROVAL_REQUIRED`.
