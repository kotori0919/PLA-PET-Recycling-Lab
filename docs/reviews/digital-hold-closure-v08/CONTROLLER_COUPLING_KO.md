# 실제 히터 제어기와 수치 열모델 연결

## PR 실패와 재발 방지

재개 HEAD a2747cdf에서 PR #4의 최신 CI-LIGHT 실행34864730099는 SUCCESS였다. 직전649d0194 실행34861143561도 SUCCESS다. 24208c7f 실행34858627442의 실패 로그는 current firmware evidence mismatch를 가리킨다. 기본 펌웨어뿐 아니라 GGM 변형 사본과 manifest를 같은 커밋에 포함해야 한다. 기존 pre-push hook과 커밋 사본 검사를 유지하며 메일·필수 검사·실패 알림 설정은 변경하지 않는다.

## 이번 구현

power_loop_bridge.cpp는 생산용 HeaterController와 HeaterPowerAllocator를 직접 host 공유 라이브러리로 컴파일한다. coupled_replay.py가 축방향 유한체적 온도를 입력하고, 반환된 각 채널의 ON/OFF를 100/100/100/60 W 열입력에 적용한다. 센서 표본250 ms와 수치 적분 시간 간격을 분리한다. 50 ms 제어 호출은 계산 조건이며 실제 AVR 실행 주기를 측정한 값이 아니다. MachineSupervisor의 호출 순서를 복제한 bridge이지 전체 펌웨어 실행은 아니다.

NaN 주입은 JSON에서 null과 invalid_channels로 기록하며 비표준 JSON NaN/Infinity를 허용하지 않는다. 개방된 열차단 신호·센서 NaN·permission 상실 후 출력을 별도로 검증한다. GPIO, 시리얼, 실제 보드 업로드나 통전은 없다.

## PI 변경 근거

기존 Ki0.08과 적분 상한500은 오차0에서 40%까지만 유지 출력을 만들었다. 상한을100/Ki로 정의하고 출력 포화 방향으로 더 쌓이는 적분을 제한한다. 비교 계산을 통해 Kp4.0, Ki0.02의 디지털 기준을 선택했다. 외부 전력 제한 추종률은0.028/s로 유지한다. 모델에서의 유효성은 실물 gain 적합성이나 안전 인증이 아니다.

4 C/120 s 가열 진행 기준과285 C 과온 기준을 바꾸지 않았다. 가열 진행 관측은 목표보다4 C 이상 낮은 상태에서 적용하고, 목표 근처의 유지 출력을 가열 실패로 오인하지 않게 한다. 정지된 저온 입력·과온·permission 상실·비유한 입력을 거부하는 회귀시험을 유지한다.

## 열량 부족을 제어기 문제와 분리

steady_state.py는 네 센서의 목표온도를 구속해 각 히터의 필요한 정상상태 전력을 역산한다. 독립 선형 star-network 이론해, 무손실 평형, 에너지 수지와 격자 세분화로 검사한다. 접촉200/1000, 외부 대류8/15, 지지 방열0.05/0.2 조합에서 일부 경우는 필요한 전력이 현재100/100/100/60 W를 넘는다. 이를 PID 숫자로 숨기지 않는다.

## 결과의 의미

이전 적분 범위 확장만 적용한 초안은 수정 형상의8조건 모두에서 가열 진행 오류로 멈췄다. 현재 PI의 같은8조건 중 정상상태 열량이 충족되는2조건은 목표온도를 유지한다. 남은6조건은 필요한 정상상태 전력이 부족하다. 가장 불리한 역산 결과는 Z1 약152.25 W, Z3 약109.75 W, die 약66.09 W이며 현재 정격보다 크다.

접촉1000, 대류8, 지지방열0.05 조건에서 최종1분 최대 센서 오차는 약0.18 C, 히터 최고온도는 약292.31 C다. 접촉200의 대응 조건은 목표 추종이 가능해도 히터 최고온도 약336.61 C이므로 공급자 확인 없이300 C 정격 적합으로 판정하지 않는다. 13 s 센서 지연 민감도도 별도다. 이 수치는 측정된 물리 상·하한이 아니다.

EXTRUSION cap300 W를 처음부터 적용한 냉간 시작 민감도는 실제 정상 진입 절차가 아니다. 다만 평균 전력 할당과 동일 위상 ON/OFF 후단의 순간 차단이 다르다는 추가 디지털 문제를 드러낸다. 네 채널이 같은 순간 ON일 때 총360 W이므로, 300 W 조건에서 단순 후단 누락은 할당된 평균 duty를 보존하지 못할 수 있다. 이 부분을 가열계 전체 PASS로 처리하지 않는다.

## 미완료 디지털 항목과 도구 제한

새 공유 전력 스케줄러의 구현 요청은 도구에서 차단됐다. 작성 도중인 header/cpp는 검사 전 기준본으로 복원했고 초안은 .build/digital-closure-20260915/blocked-scheduler에만 보존했다. 변경된 스케줄러를 배포하거나 다른 경로로 우회하지 않았다.

후방 C형 지지의 추가 포획 검사 파일 작성 요청도 차단됐다. 기존 CAD는 유지했다. 읽기 전용 FreeCAD 시험에서 후방 상부를 단순 복원한 crown은 FeederHousing, FeederAuger, FeederAgitatorDriveShaft, FeederAugerSpringPin과 겹쳤다. 이 후보를 통합 형상으로 채택하지 않았다.

후방 지지의 방사방향 접촉·강도, 뚜껑 레일/래치/인터록, 센서 체결 상세, 전력 스케줄러는 여전히 디지털 작업이다. 사용자에게 물리 blocker라는 이름으로 넘기지 않는다. physical_validation_state=NOT_RUN, machine_release=HOLD를 유지한다.

## 재현

`python3 analysis/thermal_revision_v08/run_controller_replay.py`는 수치·소스 무결성을 검사한다. process_targets_held, steady_demand, design_acceptance는 별도의 설계 판단이다. 수치 PASS가 모든 민감도 조건의 공정 PASS는 아니다. 관련 코드와 생성 결과를 같은 커밋으로 배포하고 독립 Git snapshot CI가 통과해야 push한다.

## 방법 참고

- MathWorks, Anti-Windup Control Using PID Controller Block: https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html
- Tempco, Duraband Heater Specifications and Tolerances: https://www.tempco.com/Tempco/Resources/Engineering-Data/Specifications-and-Tolerances/Duraband-Heater-Specifications-and-Tolerances.htm

일반 제품군의 외피 정격을 현 주문품의 승인 정격으로 대신하지 않는다. 이 문서의 근거는 실제 계산 결과와 명시한 수치 가정이다.
