# IF-020 extruder thrust stack 선정·검증 근거

상태: `PASS_DIGITAL / PHYSICAL_NOT_RUN / PROCUREMENT_HOLD`

## 선택 계약

- bearing: NSK 51102 single-direction thrust ball bearing, flat seat, ISO Normal
- 공칭 치수: d15 × D28 × T9 mm, 질량 약0.023 kg
- 정격: Ca10,600 N, C0a16,800 N
- screw: Ø15 h6 ×11 mm seat, Ø23.00–23.05 ×9 mm integral shaft-washer abutment,
  abutment fillet R0.3 이하
- EX-THR-01: Ø17.20 through passage/housing abutment, Ø28.30–28.35 ×
  9.10–9.15 mm marked-face pocket
- 조정: 수령 bearing 높이를 측정한 뒤0.05–0.30 mm ground steel shim으로
  loaded-direction endplay0.05–0.15 mm를 설정한다. 임의 washer나 출력물 shim은 금지한다.

NSK 제품 페이지가 명시하는 da(min)23 mm와 Da(max)20 mm에 대해 screw 최소
abutment23.00 mm, plate abutment17.20 mm다. NSK 일반 axial-load housing 권고는
diametral clearance0.25 mm 초과이며, D28 mm와 pocket28.30–28.35 mm의 계산
clearance는0.30–0.35 mm다.

## 하중 screen

6 MPa가 barrel 최대 bore Ø16.22 mm에 막힌다는 보수 조건에서
`F = p·πd²/4 = 1,239.775 N`이다. 따라서 dynamic rating SF=8.55,
static rating SF=13.55다. screw peak torque13.542 N·m와 별도 Ruland
MCLX-12-12-F 105 N·m 정격의 단순 비는7.75지만 motor-side donor fit은
IF-008이며 이 문서가 닫지 않는다.

FreeCAD source에는 Ø23 shoulder, 51102 envelope 및 깊이9.15 mm pocket을 직접
모델링했다. `validation/manufacturing_checks.py`는 active flight OD와 shoulder를
분리 검사하고, `validation/final_v08_cad.py`는 pocket 축·X389 datum·전체 조립
간섭을 검사한다. `check_extruder_thrust_stack_candidate.py`는 위 정격·abutment·
clearance와 source hash를 검증한다.

## 남은 물리 gate

구매·가공·운전 승인은 아니다. 수령품 marking/d·D·T, pocket 치수·직각도,
washer rib blue-check, shim 기록, 자유회전, loaded-direction endplay 및 heater-off
30분 추력 proof를 확인하기 전 실물 상태는 `NOT_RUN`이다. 단방향 thrust bearing은
radial load를 받지 않으므로 radial support 또는 donor coupling 검증으로 전용하지 않는다.

## 공식 출처

- NSK 51102 제품/정격/abutment: https://www.nsk.com/engineering/products/bearings/ball-bearings/thrust-ball-bearings/single-direction-thrust-ball-bearings/51102-tb-sd.html
- NSK bearing tolerance 개요(ISO 199 thrust bearing): https://www.nsk.com/tools-resources/abc-bearings/bearing-tolerances/
- NSK 일반 thrust-ball-bearing housing fit 권고: https://www.nsk.com/content/dam/nsk/am/en_us/documents/bearings-americas/Bearing-and-Linear-Replacement-Guide.pdf
