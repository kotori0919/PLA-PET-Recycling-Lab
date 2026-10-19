# PPR v0.8 직접 코드 수정 및 수치 재검증

관찰·실행: 2026-09-09 KST. 작업 머신 mathcat, 원본 /home/monad/develop/PPR.
기준 HEAD: e03e843fe3f8ce98edf7dcd26292200c3547a9d8. dirty 작업트리의 선택 원본을 별도 폴더에 복사해 시험한 뒤 해시 비교 후 적용했다.

## 실제 변경
- validation/evidence_freshness.py: 선언된 JSON 의존성을 전이적으로 추적하고 CAD 원본 및 해석용 STEP 해시를 검사한다. 빈 manifest, 경로 이탈, 순환, 잘못된 해시, 검사 중 변경을 거부한다. CURRENT는 물리적 PASS가 아니다.
- validation/v08_full_compliance.py: 고온부·축 위상·retainer·CAD·OpenModelica 증거에 위 검사를 결합했다. 수치 안전율과 제작 승인 기준은 낮추지 않았다.
- analysis/final_validation/beam_torque_recovery.py: 직선 X축 RECT B31 surrogate의 확장 절점 RF에서 반력 토크를 측정한다. 입력 토크를 결과로 복사하지 않는다.
- analysis/final_validation/run_calculix_v08.py: 측정 토크를 반력 합산에 연결하고 추가 코드·CAD·파라미터 의존성을 기록한다. 실제 keyed/contact load-path 상태는 HOLD를 유지한다.
- analysis/final_validation/run_runtime_mechanics_audit.py 및 시험 파일 2개를 추가했다.

## 실행 결과
- 무결성 unit test 19/19, 토크 추출 unit test 8/8 PASS.
- 기존 shaft reaction provenance 시험 및 26절 coverage self-test PASS.
- 실제 CalculiX 2.23 실행 50회에서 JOB FINISHED 확인: 별도 수치 감사 28회 + core clean rerun 22회.
- 28회 감사: 축 mesh 9회, 토크 부호/크기 3회, 열·추력·spring 조건 16회. 잘못된 토크 3개 부정 대조 거부.
- 축 토크 최대 잔차 1.792e-5 N.m. LC02 driven fine: 적용 +22, 측정 -22.00001792 N.m.
- LC04 fine 변위 0.0012606543458918349 mm 재현. core 최종 상태는 LC02 HOLD / LC04 PASS / LC05 HOLD / hot-zone HOLD.
- 열팽창 해석/손계산 최대 상대차 2.654e-7. 이는 같은 선형 surrogate의 계산 검증이지 실제 재료·온도장 검증이 아니다.

## 중요한 새 관찰
기존 가정 alpha=17e-6/K, L=280 mm, 기준25°C에서 전체 길이 팽창은 270°C에서1.1662 mm, 300°C에서1.309 mm다. 6 MPa 추력을 더한 같은 B31 모델은300°C에서1.311602 mm를 보였다. 명시된 최소 travel1.30 mm와의 산술 차이는 -0.011602 mm다.
이는 실제 guide 간섭 확정이 아니다. 물성의 근거, 실제 온도장, 제한 접촉면과 팽창 기준 길이를 먼저 연결해야 한다. alpha나 CAD travel, 재료 허용강도를 임의 수정하지 않았다.

## 통합 판정과 후속 연결
통합 gate를 실제로 실행하되 출력은 이 검토 폴더로 격리했다. aggregate_check.json은18/25 FAIL이다. 원래의20/25는 변경 전 생성 결과다. 이번 runner 변경으로 이를 참조하는 기존 수치 증거는 재실행/정식 승계가 필요하며, 새 검사기가 이를 자동 PASS시키지 않는다. 새 기계 결함이 두 개 확정됐다는 의미가 아니다.

수정 전 선택한6개 증거 그래프는 선언된 해시 경로에서 CURRENT였다. 이전 steering의 일부 stale 결과는 기존 작업자가 이미 재생성했다. 이번 변경은 그 재발 방지용이다.

최종 코어 결과를 canonical summary.json에 강제 덮어쓰지 않았다. core_clean_rerun_summary.json과 runtime_mechanics_result.json에 재실행 결과가 있고, 실제 원시 결과의 루트 상대 경로는 evidence_locations.json에 있다. 209개 INP/FRD/DAT/log 해시는 run_evidence_manifest.json에 기록했다.

남은 핵심은 SCM440 고온 물성/온도장 근거, die joint 고온 예압·접촉, 실제 keyed shaft 하중 경로, TS-15/16, 미선정 drive interface와 완전한 interface coverage다. 물리 수령·시험과 디지털 설계 정의를 구분해서 닫아야 한다.

## 파일
- change_log.json: 변경 파일7개 및 전후 해시.
- code_changes.patch: 이번 수정만 포함한 diff.
- before/: 기존 수정 파일2개의 적용 전 내용.
- test_results.json: 실제 원본 저장소에서 수행한 시험 로그.
- integrity_before.json: 적용 전 해시 그래프 관찰.
- core_clean_rerun_summary.json: 수정된 core 실제 실행 결과, HOLD 보존.
- runtime_mechanics_result.json: 추가28회 수치 감사 결과.
- aggregate_check.json / aggregate_check_ko.md: 강화된 통합 검사.
- run_evidence_manifest.json / evidence_locations.json: 원시 실행 파일의 위치와 해시.

격리 작업 폴더: /home/monad/develop/PPR-assistant-work-20260909T2328.
기존 CAD·재료·공차·펌웨어·패키지와 실행 중인 다른 agent를 수정하거나 종료하지 않았다. 설치, Git add/commit/push/merge, 게시, 구매, 하드웨어 통전은 하지 않았다. 모든 계산 프로세스는 종료됐다.
