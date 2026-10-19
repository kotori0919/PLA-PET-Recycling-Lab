# IF-022 기준 feeder drive 계약

- 디지털 기준품: StepperOnline `17E1K-07` closed-loop NEMA17 motor + `EG17-G10` 10:1 gearbox + `CL42T-V41` driver.
- 근거: motor 0.72 N·m holding torque, 2.0 A/phase, Ø5×24 shaft, 42×42×80; gearbox 10:1, 효율96%, 연속 허용5 N·m, Ø8 keyed output×21.5, 42×42×55; driver 24–48 VDC, 0–3 A peak, STEP/DIR/ENA 및 ALM.
- 공급사 원문: https://www.omc-stepperonline.com/tp-series-1-axis-closed-loop-stepper-cnc-kit-72ncm-101-98oz-in-nema-17-motor-1-cl42t-p07-v41 ; https://www.stepperonline.co.uk/eg-series-planetary-gearbox-gear-ratio-10-1-backlash-15arc-min-for-nema-17-stepper-motor-eg17-g10.html ; https://www.omc-stepperonline.com/download/CL42T-V41_user_manual.pdf

## 설계 판정

- gearbox 연속 허용 토크 기준 여유는 `5/2.2 = 2.273`; 기존 feeder 설계 토크 2.2 N·m에 대해 SF≥2다. Motor의 정지 holding torque를 운전 토크로 대체하지 않는다. 18–22 motor rpm 구간의 실제 토크는 입고 후 torque-arm 시험으로 확인한다.
- `FD-DA-01` 8 mm steel welded shelf가 drive 반력을 우측 20×20 frame post로 전달한다. Hopper sheet/출력물이 하중 경로가 아니다.
- `FD-CP-01`은 gearbox Ø8 keyed output과 FD-MET-03 상단 Ø3 cross-pin을 잇는다. Set-screw 마찰만으로 토크를 전달하지 않는다.
- 5 N·m는 gearbox 제품 한계이며 기계 운전 명령은 2.2 N·m 검증 창을 넘지 않는다. ALM, A7 tach-loss 또는 안전 체인 open 시 다음 supervisor cycle에서 command를 0으로 한다.

## 전장·firmware 계약

- CL42T: 24 VDC, 800 pulse/rev, single-pulse STEP/DIR, 5 V opto-input selector. D44 STEP, D42 DIR, D46 ENA, D47 ALM(active-low), A7 output-shaft tach다.
- 공통축 surrogate의 material-form 평균값을 반올림한 초기값은 PLA 6.6 rpm, PET 8.0 rpm이며 STEP rate는 각각 880/1067 Hz다. 이는 실측 보정 전 reference default다. Firmware는 200 ms DIR/ENA setup 뒤 Timer5 OC5C에서 50% duty pulse를 생성한다.
- PUL/DIR/ENA는 각각 NPN open-collector interface와 base resistor/pulldown을 거쳐 연결한다. Mega pin에서 driver optocoupler를 직접 구동하지 않는다. ALM은 sinking output과 D47 pull-up을 사용하며 실제 polarity를 bench에서 강제 확인한다.
- A7은 독립 24 PPR output-shaft tach의 conditioned 5 V output을 받는다. 4.0 rpm 설계 하한의 nominal edge interval은 0.625 s로 2.0 s timeout 안이다. Tach 후보 MPN/level은 아직 미선정이므로 구매·energization은 HOLD다.

## 남은 물리 gate

주문·비용 지출은 승인되지 않았다. 입고 후 shaft/pilot/hole pattern, 24 V current, driver input/ALM polarity, 18–22 rpm torque curve, coupling TIR, 24 PPR tach, 2.2 N·m torque-arm 및 10회 hand-turn을 확인하기 전 제작·통전·운전 PASS를 주장하지 않는다. 다른 motor/gearbox/driver는 FD-DA-01, FD-CP-01, pulse rate, current/fuse와 torque SF 재계산 없이는 대체할 수 없다.
