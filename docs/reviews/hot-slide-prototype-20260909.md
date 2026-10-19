# 고온부 sliding prototype 실행 종료 — 2026-09-09

## 결과 위치
선정 소스와 시험치구는 `experiments/hot_slide_r1/`에 있다. 압축 파일은 `dist/PPR-HS-R1-S2-TEST-FOUNDATION-20260909.zip`이다.
ZIP SHA-256: `515bb6182fb5eb96b1630f939f2cc4ab45a6c43a4c494d8f193137b71fdb552f`.
크기4,416,088 bytes, payload78개. 실제18개 solver run, 원시 핵심 입력/출력72개 hash, 합성 protocol test26개를 포함한다.

## 기술 판단
HS-R1-S2는 세 탄성 슈, 방사형 슬롯과 shoulder-pin 비압착 stack을 갖는 독립 무가압 시험치구다. 확대 보어만 사용하는 해법이 아니다. 기존 axial shoulder/retainer를 대체하지 않았고, 전체 기계 설치도 승인하지 않았다.
선정 형상 기본12회 및 prescribed gradient6회의 C3D10 계산을 수행했다. 6,144개 대수 조건과 별도 보어 완화 후보48개 자유팽창 부품쌍 검사도 수행했다. Solver STEP과 prototype 제작 STEP의 symmetric difference는0이다.
계산 중심 변위 상한0.04422 mm에 실물 달성 요구인 설치 예산0.040 mm를 더하면0.08422 mm다. 조건부 최소 슈 법선력2.073 N이다. 고온1,100 MPa 요구는 계산에서 도출한 잠정 재료 요구이지 구매 재료의 인증값이 아니다. 실제 마찰·접촉·피로·온도장 및 두께방향 peak 수렴은 아직 적격성 미완료다.
300 N은 제안한 시험 중단 기준이며 검증된 구조 하중 정격이 아니다. 체결부·치구·원재료의 사전 검토 없이 이 힘으로 시험하지 않는다. 실제 물리 측정 template은 NOT_RUN이다.

## 기존 작업 보존
이번 선택 작업은 새로운 experiments 디렉터리와 검토 기록에 한정했다. 관찰한 active CAD/parameter/solver/release-note 원본9개는 시작 hash와 동일했다. 기존 제작 ZIP/active design/과거 검증 결과의 PASS를 덮어쓰지 않았다. Main merge, commit/push, 구매, 가공, 가열 또는 회전은 수행하지 않았다.
전체 PPR release는 HOLD이며 별도 전체 compliance 재실행을 완료했다고 주장하지 않는다. Prototype package integrity PASS와 기계 제작 PASS는 다르다.

## 다음 판정 경로
재료/가공 승인 후 먼저 압력·회전 없는 냉간 치구 시험으로 실제 중심 정렬과 시작/유지 마찰을 확인한다. 가열 시험은 독립 보호, 온도 계측, 재료 근거와 별도 승인 후에 진행한다. 결과가 확보된 뒤에만 실제 PPR 지지체/추력 경로/guard/축 정렬에 통합하고 동일 설계에서 검증 산출물을 갱신한다.
