# GMP60 기준 구동 인터페이스 근거 — v0.8

## 범위와 상태

`TT Motor GMP60-60127-2460`, 24 V, 감속비 47을 **교환식 구동계의 디지털 기준 변형**으로 사용한다. 이 문서는 구매 승인, 수령 합격 또는 물리 Gate-1 완료를 뜻하지 않는다. 실제 구매에는 사용자 승인이 필요하고, 수령품이 아래 합격범위를 벗어나면 `DRV-A60`/`DRV-F01A`를 억지로 조립하지 않고 새 `DRV-Axx`/`DRV-F01Axx` 편차를 발행해 IF-008을 다시 검증한다.

## 제조사 공개 nominal

제조사 도면: <https://www.ttmotor.com/uploads/GMP60-609760127.pdf> (2026-09-09 확인)

| 항목 | 공개값 |
|---|---:|
| 전압 / 감속비 | 24 V / 47:1 |
| 무부하 / 정격 속도 | 95 / 70 rpm |
| 정격 토크 / 전류 | 100 kg·cm = 9.80665 N·m / 8.2 A |
| stall current | 31 A |
| motor / gearbox | Ø60.5×127 / Ø60×59 mm |
| front pilot | Ø32×4.85 mm |
| 출력축 | Ø12×25.8 mm, D-flat 길이 13 mm, across-flat 10.9 mm |
| 체결 | 4×M5, PCD45 mm |

공개 도면은 이 인터페이스에 필요한 공차를 보증하지 않으므로 nominal을 그대로 끼워맞춤 보증으로 사용하지 않는다. 아래 수령 합격범위와 제작 한계가 계약값이다.

## 수령 합격범위와 제작 한계

| 형상 | 수령품 합격범위 | 제작품 한계 | 계산된 간극 |
|---|---:|---:|---:|
| motor pilot / DRV-A60 bore | Ø31.95–32.00 | Ø32.05–32.10 | 직경 0.05–0.15 mm |
| motor shaft / DRV-F01A circle | Ø11.95–12.00 | Ø12.02–12.05 | 직경 0.02–0.10 mm |
| shaft / hub across-flat | 10.85–10.90 | 10.92–10.95 | 0.02–0.10 mm |
| motor / adapter bolt pattern | PCD44.90–45.10, M5 major Ø≤5.00 | 4×Ø5.50–5.60, PCD45.00±0.05 | 조립 시 각 홀 자유 통과 확인 |

`DRV-F01A`의 D-bore는 처음 13 mm에서 토크를 전달하고 나머지 3 mm는 Ø12.04 nominal 원형 relief다. Pilot bore는 Ra≤3.2 µm, D-bore는 Ra≤1.6 µm로 마감한다. Set screw 마찰만으로 토크를 전달하지 않는다.

## D-flat 정적 screen

- motor-side relief 설정: 10.35 N·m
- D-flat 중심거리의 보수값: 4.90 mm
- 접선력: `10.35 / 0.00490 = 2,112 N`
- nominal 원의 D-flat chord: `2×sqrt(6²−4.9²) = 6.93 mm`
- 13 mm 접촉 투영면적: `6.93×13 = 90.1 mm²`
- 평균 bearing stress: `2,112 / 90.1 = 23.4 MPa`
- S45C hub의 보수 허용 bearing stress를 120 MPa로 둔 screen SF: `120/23.4 = 5.13`

이는 nominal 정적 계산이며 충격, 실제 접촉분포, 재료 성적서와 마모 시험을 대신하지 않는다. 물리 Gate-1에서 blue-check 접촉, TIR, 20회 손회전, 저속 current/torque calibration과 relief 작동을 확인한다.

## 판정

명시된 수령 범위 안의 GMP60 기준 변형에 한해 IF-008의 치수·양의 토크 경로는 디지털 `PASS`다. 구매, 수령검사, energization과 Gate-1은 `NOT_RUN/HOLD`다.
