# 물리 검증·시제품 제작 착수용 검증 계획

기준: PPR `final-design-fabrication-closure-v0.8` HEAD `34ae29d7` + 미커밋 작업 트리(컴팩트 배치, 2026-10-19). 방법론은 `hardware-verification-plan` skill(L0-L5)이다. 이 문서는 물리 검증 완료, 구매·가공·통전 승인, 안전 인증이 아니다. 상태 어휘: OBSERVED(이번 실행에서 관찰), MEASURED(실측), INFERRED, PROPOSED, NOT_RUN.

## 1. 요약

진단: 디지털 gate 증거는 풍부하지만(25항목 compliance, P1-P12 analyzer 15개, 단위·회귀시험 다수) 작업 트리의 컴팩트 배치(GGM-FULL-ASM 470x700x930)가 바뀌면서 프레임 절단표 바인딩이 낡았다. OBSERVED: `frame_release.py`가 `stale frame binding: exports/final/drive_ggm_v08/manifest.json`으로 실패했고 compliance는 22/25였다. 즉 P2 절단계획의 입력이 최신 CAD와 어긋난 상태로 P1/P2에 들어갈 수 있었다. 이 결함은 비싼 도구가 아니라 L0 해시 게이트가 잡는 것이며 실제로 게이트가 잡았다.

이번 조치(OBSERVED):
1. `analysis/frame_v08/audit_geometry.py` -> `beam_screen.py` -> `release/build_frame_release.py`를 현재 CAD로 재실행해 프레임 바인딩을 갱신했다. 절단 물량은 불변(2020 36개/15,078 mm, 2040 4개/2,180 mm; 이전 `frame_cut_list.csv`와 byte 동일).
2. `frame_release.py` 결과 `FRAME_CUTLIST_BINDING_PASS`, `simulation_prerequisite.py` 결과 `PHYSICAL_V08_DIGITAL_PREREQUISITE_PASS technical=23 failed=0`, compliance 23/25.
3. 낡은 외형 서술(Y729, "선호 Y720보다 9 mm 큼")을 현재 CAD 값 470x700x930 mm(nominal)로 정정했다.

남은 compliance 2건은 `20_release_package`(ZIP 재생성)와 `21_release_policy`(원격 HEAD/PR 확인)이며 설계가 아니라 배포 절차다. `simulation_prerequisite`도 이 둘을 제외한다. 커밋·재패키징 후 별도로 다시 판정한다.

범위: 구매·가공·통전 승인과 물리 시험 판정은 다루지 않는다.

## 2. 지금 바로 시작 가능한 것 / 불가능한 것

| 작업 | 상태 | 근거 |
|---|---|---|
| P1 무가공 재고·치수 조사 (bar별 usable length, 구매품 라벨) | 시작 가능, 승인 불필요 | `PHYSICAL_EXECUTION_INDEX_KO.md` "실제 첫 행동"; 절단 없음 |
| P2 nesting 계획 작성 | P1 실측 후 | `frame_release.json`의 `stock_nesting=ACTUAL_RECORDS_REQUIRED` |
| 프레임 절단·조립 (S3) | 사용자 fabrication 승인 필요 | `cut_authorization=false` 유지 |
| GGM 모터 구매 (S2) | 사용자 구매 승인 필요 | AGENTS.md: 승인 없는 주문 금지 |
| P3 bench 통전 | 사용자 통전 승인 + lockout | donor/GGM 라벨 실측 선행 |
| P4 cutter 2장, P5 coupon 주문 | 사용자 승인 필요 | 본품 전량 발주는 P5 합격 후 |

## 3. 검증 층별 현황

| 층 | 현재 오라클 | 상태 |
|---|---|---|
| L0 계약·해시 | `v08_full_compliance.py`(25), `frame_release.py`, `configuration_control.py` | 23/25 OBSERVED; 20/21 배포 절차 |
| L1 기구 | 구속 자코비안 해석기 없음. OpenModelica/FreeCAD 모션 샘플 | 부분. 아래 공백 G1 |
| L2 연속 기하 | `integrated_assembly_clearance`, `integrated_motion_clearance`(샘플링, "not a continuous angular proof") | 샘플 기반. 공백 G2 |
| L3 구조·체결 | 폐형식 + CalculiX 수렴 해석 기록, 프레임 joint는 `joint_strength_qualified=false` | 비교 screen만. 프레임 강도는 NOT_RUN |
| L4 시스템 | runtime supervisor harness, 펌웨어 HEX 재빌드, 열 모델 | CI-FULL 범위. 신규 solve 아님 |
| L5 실측 | P1-P12 analyzer + typed record 템플릿 | 전부 NOT_RUN |

## 4. 공백과 작업 패키지

| ID | 공백 | 변경 파일(제안) | 합격 기준(제안, 사용자 결정) | 실행 |
|---|---|---|---|---|
| WP-0 | (해소됨, OBSERVED) 프레임 바인딩 stale 검출은 이미 `v08_full_compliance.py` 07항목과 prerequisite에 연결되어 실제로 22/25 FAIL을 냈다 | 변경 없음 | stale 시 FAIL | CPU, 수 초 |
| WP-1 (G1) | 연결 도달성/이동도 오라클 부재 | 신규 `validation/mechanism_graph_check.py` (기존 manifest 재사용) | 도달 불가 그룹 0 | CPU |
| WP-2 (G2) | dancer/cutter 위상 샘플 간 보장 없음 | `integrated_motion_clearance.py`에 최소 거리 하한 출력 추가 | 전 행정 최소 거리 > 사용자 지정 여유 | CPU |
| WP-3 | P1 실측 입력 형식 검증 | 기존 `analyze_p1_records.py` + `profile_nesting.py` 사용 | 템플릿 NOT_RUN 유지, 실측 입력 후 PASS | CPU+수동 |
| WP-4 | 계측기 정확도(%GRR) 미확인 | `measurement_equipment.csv`에 MSA 열 추가 제안 | 공차 +/-0.05 mm 항목은 %GRR <= 30% (제안) | 수동 |

WP-1~2는 PROPOSED이며 이번 변경에 구현하지 않았다.

## 5. 기존 실패 -> 패키지

| 기록된 실패 | 내용 | 먼저 잡는 패키지 |
|---|---|---|
| compliance 22/25 (OBSERVED, 2026-10-19) | 프레임 바인딩이 새 GGM manifest 해시와 불일치 | L0 `frame_release.py` (이번에 해소) |
| 문서 서술 불일치 | 문서 Y729 대 CAD Y700 | WP-0 계열 문서-CAD 값 대조(미구현) |

## 6. 테스트 계획 (요지)

- 단위/게이트(수 초, 매 커밋): `validation.test_frame_release`(4건 OK, OBSERVED), `test_fabrication_active_part_set`(4건 OK, OBSERVED).
- FreeCAD 시스템 시험(수 분): `test_integrated_assembly_clearance`, `test_integrated_motion_clearance`, `test_native_model_handoff`, `test_assembly_refresh`, `test_frame_reduction_geometry`, `test_compact_fixed_foot`. 재생성한 프레임 바인딩과 현재 작업 트리 CAD에서 6건 모두 통과(OBSERVED; `test_compact_fixed_foot`은 unittest `SystemExit(0)`). 간섭 시험은 nominal 솔리드 기준이며 물리 검증이 아니다.
- 실물(승인 하): P1 -> P2 -> P3 순서는 `fabrication_sequence.csv`가 controlling.

## 7. 에이전트 운영 규칙 (이 저장소 적용안)

1. 설계·반증 에이전트는 PASS를 쓰지 않는다. 판정은 오라클 스크립트와 사람 리뷰어.
2. 결과는 JSON으로, 대상 commit과 입력 해시에 묶는다. 이번 프레임 재생성은 미커밋 작업 트리 기준이므로 커밋 후 `generation_base_commit`을 재확인해야 한다.
3. 가상 결과로 NOT_RUN 실측 상태를 채우지 않는다. 합격 기준을 실패 후 완화하지 않는다.

## 8. 사용자 결정 체크리스트

- [ ] 현재 미커밋 컴팩트 배치(Y700)를 v0.8 제작 기준으로 채택하는가 (HEAD의 release 문서는 Y729 기준이었음)
- [ ] 이번 재생성 산출물(FR-TIE-01 STEP/DXF/FCStd, frame_release.json)의 커밋 시점
- [ ] WP-1/WP-2 구현 여부와 최소 거리 여유값
- [ ] S2 GGM 모터 구매 승인, P1 재고 조사 착수
