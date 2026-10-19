# 470 x 700 x 930 mm compact 배치의 canonical 승격

## 목적

이 revision의 제품은 산업용 압출 설비를 축소하는 것이 아니라, 하나의 프레임 안에서 PLA/PET의 분쇄, 정량공급, 압출, 냉각/측경, 권취를 수행하는 벤치형 최종 제품이다. MVP와 최종 제품은 같은 실물이다. 명목 feed-control 목표는 100 g/h이며 200 g/h는 stretch 목표다. stretch 목표만을 위해 외형, 히터 또는 PSU를 키우지 않는다.

기존 GGM 통합 형상의 470 x 729 x 930 mm 중 추가 29 mm 깊이는 주로 분쇄 모터 쪽 돌출에서 발생했다. 상부 shredder/input 경로를 프레임 안쪽으로 X -18 mm, Y +29 mm 이동하고, FlakeBin/PPR-C03 collection path는 X를 유지한 채 Y +29 mm 이동한다. MidRail500, GGM_ShredRail 및 네 개의 shelf support spacer는 기존 프레임 datum을 유지한다. GGM_SH_Base는 동일한 6 mm 판 외형/체적을 사용하고 moved post 축에 맞춰 네 개의 M5 hole만 재배치한다.

결과 외형은 **470 x 700 x 930 mm**다. 729 mm 기준 대비 bounding volume은 약 3.98% 줄고 preferred envelope 480 x 720 x 950 mm 안에 들어간다. 이 상태에서 추가적인 폭/높이 축소는 현재 목적에 필요하지 않으며, 정비성이나 구조성을 희생하는 축소는 진행하지 않는다.

## 디지털 근거

- 266-object nominal geometry와 35,245 pair collision audit에서 새로운 미분류 간섭은 0건이다.
- fixed-foot candidate와 canonical assembly의 각 solid는 양방향 차집합 기준 0.01 mm3 이내로 동일하다.
- 전체 frame response 비교는 frame identity, global/local compliance 및 refinement 조건을 통과한다.
- support datum/접촉 위치와 네 fixed spacer는 기존 위치를 유지한다.
- GGM shelf의 기존 C3D4/C3D10 국부 해석은 solver/equilibrium은 통과했지만 displacement mesh convergence를 만족하지 못했으므로 FAIL diagnostic로 그대로 보존한다.
- 이를 PASS로 바꾸지 않고, 각 100 N post comparison load를 가장 가까운 fixed spacer까지 폭 20 mm, 두께 6 mm의 독립 cantilever strip으로 보내는 더 단순하고 보수적인 screen을 추가했다. 최악 L=67.624 mm에서 stress 56.35 MPa, deflection 0.1432 mm, S275 yield SF 4.88이며 SF=2에서의 per-post comparison load limit은 약 244 N이다. 실제 운전하중을 100 N이라고 주장하는 근거는 아니며 P3 실측은 별도다.

machine-readable 판정은 `analysis/compact_layout_v08/results/canonical_promotion.json`이다.

## 남는 물리 경계

이번 승격은 실제 GGM 질량/진동, 수령 fastener engagement, P2 frame squareness, P3 운전/jam 하중, guard/service 접근의 실물 확인을 대신하지 않는다. `physical_validation_state=NOT_RUN`, `fabrication_authorized=false`, `energization_authorized=false`를 유지한다.
