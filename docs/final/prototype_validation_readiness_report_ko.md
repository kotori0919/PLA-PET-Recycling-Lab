# 시제품 제작·물리 검증 착수 준비 보고서

기준: PPR `final-design-fabrication-closure-v0.8`, 브랜치 HEAD `95832b99` (2026-10-19). 방법론은 `hardware-verification-plan` skill(실행·보고 모드, L0-L5)이다.
이 문서는 디지털 설계의 착수 준비 상태를 보고한다. 물리 검증 완료, 구매·가공·통전 승인, 안전 인증이 아니다. 상태 어휘는 OBSERVED(이번 실행에서 관찰), MEASURED(실측), INFERRED(추론), PROPOSED(제안), NOT_RUN(미수행)이다. MEASURED 항목은 현재 없다.

## 1. 요약

진단. 디지털 증거(25항목 compliance, 13항목 릴리스 인벤토리, P1-P12 분석기)는 완비되어 있으나, 작업 트리의 컴팩트 배치(GGM-FULL-ASM 470x700x930 mm)가 커밋되지 않은 채 증거 해시와 어긋나 있었다. 이번 작업에서 이를 해소했다. 결과 상태는 아래와 같다.

| 항목 | 값 | 상태 |
|---|---|---|
| `v08_full_compliance.py` | 25/25 PASS | OBSERVED |
| `v08_release_inventory.py` | 13/13 PASS | OBSERVED |
| `simulation_prerequisite.py` (P0) | 23/23 기술 gate PASS | OBSERVED |
| FABRICATION ZIP | 1,297개 파일, `verify_fabrication_release.py` PASS, source_commit = `95832b99` (보고서 커밋으로 HEAD가 바뀌므로 최종 ZIP은 보고서 커밋 HEAD로 재생성되며 해시가 달라진다) | OBSERVED |
| FreeCAD 간섭·handoff 시험 6건 | 전부 통과 | OBSERVED |
| 물리 시험 P1-P12 | 전부 NOT_RUN | NOT_RUN |
| 구매·가공·통전·가열 | 전부 미승인 | 사용자 승인 필요 |

핵심 제안 3개.
1. **지금 시작할 수 있는 것은 P1 무가공 재고·치수 조사 하나다.** 전원, 절단, 구매가 없고 템플릿과 분석기가 준비되어 있다 (4절).
2. **싼 해시 문지기가 비싼 도구보다 먼저 결함을 잡았다.** 프레임 바인딩 stale은 L0 게이트가, 증거 낡음은 pre-push 훅이 잡았다. 이 구조를 유지한다 (3절).
3. **VALIDATED는 실측 보정으로만 얻는다.** 가상 결과로 NOT_RUN을 채우지 않는다. 실패 시 합격 기준을 완화하지 않고 설계를 수정해 같은 실물로 재시험한다 (7절).

## 2. 범위표

| 하위 시스템 | 주요 경로 | 범위 | 다루는 방식 |
|---|---|---|---|
| 프레임·전체 배치 | `cad/freecad/drive_v08`, `exports/final/drive_ggm_v08`, `exports/final/frame_v08` | 포함 | 전체 재바인딩·간섭 재검증 |
| 구동계(GGM) | `analysis/drive_acceptance_v08`, `control/ggm_drive_contract.json` | 포함 | 디지털 gate 확인만. donor 실측은 P1 |
| 분쇄·압출·고온부 | `analysis/final_validation`, `cad/freecad/final_v08` | 포함 | 기록된 해석을 재감사(신규 FEA 없음) |
| 전기·펌웨어 | `electronics`, `firmware`, `validation/runtime_supervisor.py` | 포함 | 기존 호스트 시험과 인벤토리 gate |
| BOM·예산 | `bom/` | 포함 | 현황 보고. 구매 승인 아님 |
| 구형 v0.6/Fusion 실험 | `docs/fusion_*`, `exports/fusion_validation` | 제외 | 계보 보존용. 현재 인수인계 기준 아님 |

## 3. 실행·보고 기록과 재현성 관찰

### 3.1 HEAD 타임라인

| 시점 | HEAD | 내용 |
|---|---|---|
| 시작 | `34ae29d7` | 작업 트리에 컴팩트 배치 WIP 375개 변경이 미커밋 상태 |
| 1차 커밋 | `2e1a71c6` | 프레임 절단표를 컴팩트 CAD에 재바인딩, Y729 서술 정정 |
| 2차 | `bf30b90e` | 간섭·모션·hot-zone 증거 3건 재생성 |
| 3차 | `53259e18` | PR URL 기록 수정 (kotori0919) |
| 4차 | `6258b917` | 나머지 설계·BOM·검토 자료 일괄 커밋 |
| 5-6차 | `5a93c9f9`, `95832b99` | CI 시험 분류·경로 수정 |

### 3.2 실행한 검사와 결과

| 명령 | 결과 | 비고 |
|---|---|---|
| `v08_full_compliance.py` | 22/25 -> 23/25 -> 24/25 -> **25/25** | 07 stale frame binding, 21 PR URL, 20 ZIP 순서로 해소 |
| `frame_release.py` | `stale frame binding: exports/final/drive_ggm_v08/manifest.json` -> `FRAME_CUTLIST_BINDING_PASS` | 40 부재, 2020 36개 15,078 mm, 2040 4개 2,180 mm |
| `audit_geometry.py`, `beam_screen.py`, `build_frame_release.py` | 재생성 PASS | FreeCAD 0.21.2, typst 0.15.1 |
| `integrated_assembly_clearance.py` | `GGM_NOMINAL_COLLISION_POLICY_PASS` 266 objects, 35,245 pairs | nominal 솔리드 |
| `integrated_motion_clearance.py` | `GGM_NOMINAL_MOTION_CLEARANCE_PASS` | 샘플 기반 |
| `hot_zone_revision_review.py` | 재생성. 이전 값 대비 상대 오차 약 1e-13 | 물리 불변, 해시만 갱신 |
| `build_fabrication_release.py` / `verify_fabrication_release.py` | 1,297 files PASS, ZIP sha256 `78517a2d683381cb90df4d406be396f74cb73e441b852663c3c703a8d8ddadf4` | 이전 ZIP(9/14)은 스크래치에 백업 |
| pre-push 훅(light suite) | 4회 실패 후 통과 | 3.3 참조 |

환경: Python 3.15.0(호스트) / 3.12(저장소 CI 기준), FreeCAD 0.21.2, typst 0.15.1(nix store), nix develop.

### 3.3 게이트가 잡은 결함 (기존 실패 -> 잡은 층)

| 기록된 실패 | 내용 | 잡은 층 |
|---|---|---|
| compliance 22/25 | 프레임 바인딩이 새 GGM manifest 해시와 불일치 | L0 `frame_release.py` |
| pre-push 1차 실패 | `hot_zone_revision_review.json`이 이전 `assembly.py` 해시 기록 | L0 증거 폐쇄(`test_package_import_closure`) |
| pre-push 4차 실패 | `test_compact_shelf_mesh` import 경로, FreeCAD 필요 시험이 light suite에 분류됨 | CI 분류 |
| 자체 오류 1건 | 해시 묶인 `run_calculix_v08.py`를 수정해 03/05 gate가 깨짐 | 스냅샷 재검증이 잡음. 바이트 단위 복원 |
| 자체 오류 2건 | 경로 없는 `git checkout`으로 detached HEAD. 추적 변경 손실 없음, 브랜치로 복귀 | 상태 확인 |

재현성 관찰. 해시와 상태 판정은 재실행에서 재현되었다. 열 해석 trace는 float 잡음 수준(약 1e-13)으로만 달랐다. 정본 증거 4개(`v08_full_compliance.json` 등)는 재실행으로 작업 트리에서 수정된 채 남아 있으며, 이를 커밋하면 HEAD가 바뀌어 ZIP이 낡으므로 의도적으로 커밋하지 않았다.

### 3.4 아직 못한 것 (NOT_RUN)

- COMPLETE ZIP 재생성(9/14본 그대로, compliance 항목 아님).
- graphify 문서 의미 추출(`/graphify --update` 스킬). AST 갱신만 수행.
- 물리 시험 전부, FEA 신규 solve, 제3 솔버 교차 검증(범위 결정으로 미수행).

## 4. 바로 착수 가능한 작업 (P1)

P1은 전원·절단·구매가 없는 재고 식별과 치수 기록이다. 문서: `validation/physical_v08/P1_EXECUTION_KO.md`, 기록: `templates/p1_inventory_record.csv`(30개 항목 고정, 삭제·추가 금지), 분석: `analyze_p1_records.py`, GGM 대조: `analyze_ggm_mount_compatibility.py`, nesting: `profile_nesting.py`.

| 순서 | 작업 | 도구(`measurement_equipment.csv`) | 산출 |
|---|---|---|---|
| 1 | 2020/2040 각 bar의 사용 가능 길이와 U95 기록(절단 금지) | MEAS-16 장척 steel tape(1 m 이상 검증) | `profile_stock_measurement.csv` |
| 2 | 6201 x3, 61905/6905 x4, 51102 x1 각인·치수·자유회전 | MEAS-01/02 캘리퍼·마이크로미터 | 항목별 row |
| 3 | 24 V PSU, BTS7960 x2, Mega, E-stop 라벨·단자·손상 사진 | MEAS-09 DMM(비통전 연속성만) | 사진·SHA-256 |
| 4 | K0/K1, positive-opening NC 스위치 x3, 퓨즈, Hall 센서 x2, #35 체인·스프로킷 정확한 모델·정격 | 육안·라벨 | 정격 기록 |
| 5 | TH-INS-01 PI 테이프(25 mm x 30 m) 제조사·접착제·lot | 육안·라벨 | S4 coupon 입력 |
| 6 | 프레임 절단 계획 | `profile_nesting.py` | 측정 길이 - U95 - kerf(0.5 mm/개 절단 허용차) 기준 nesting |

P1 PASS 조건: GGM 두 세트 수령이 필요하므로, 미수령이면 P1은 PASS가 아니라 `PARTIAL_NOT_RUN`이다. 재고 조사 자체로는 구매·가공 승인이 생기지 않는다.

## 5. 제작·구매 순서와 승인 지점

원칙: MVP는 별도 시제품이 아니라 최종 기계 자체다. 제작과 검증을 병행하되 검증보다 제작이 앞서 downstream 형상을 고정하지 않는다. 실패한 구획과 의존 단계만 HOLD한다.

| 단계 | 내용 | 최소 수량 | 사용자 승인 지점 | 종료 조건 |
|---|---|---|---|---|
| S0-S1 | 디지털 선행 고정, 재고 조사 | 0 | 없음 | P0 PASS, 재고표 갱신 |
| S2 | GGM 모터 구매(재고로 대체 불가 시) | K9DG60N2+K9G75C, K9DG60N2+K9G150C 각 1 | 구매 승인 | P1 수령검사 PASS |
| S3 | 저비용 프레임·GGM bench fixture | 프로파일·판재·출력 가드 | 가공 승인 | P2 + P3 fixture |
| S4 | GGM 전류·토크·기계식 보호 교정 | 황동 보호 coupon 최대 9개 | fixture 통전 승인 | P3 PASS |
| S5 | 분쇄기 coupon만 제작 | CUT-01 2장 등(나머지 10장 잠금) | coupon 가공 승인 | P4 PASS |
| S6 | SCM440 공정 coupon만 발주 | EX-CPN-SCR 1, EX-CPN-BAR 1 | coupon 발주 승인 | P5 PASS |
| S7 | P4 합격 시 분쇄기 전체 | CUT-01 나머지 10장 등 | 전체 분쇄기 승인 | 기계 세트 완성 |
| S8 | P5 합격 시 screw/barrel/die 본품 | EX-SCR-01, EX-BAR-01 | hot-zone 전체 승인 | P6 PASS |
| S9 | 전기·안전, logic-only 먼저 | K0, interlock, 퓨즈, Mega, BTS | logic 통전 승인 | P7 PASS |
| S10 | 모터 건식 시험(한 축씩, heater 오프) | - | 모터 통전 승인 | P8 PASS |
| S11 | 가열기 구매·빈 hot-zone | band 3, cartridge 1, probe 5, retainer 4, TH-FUSE-01 3 | heater 통전 승인 | P9 stage release |
| S12-S13 | PLA -> PET 저속 공급, 성형·권취 | 건조된 소량 lot | 재료 공급·전체 경로 승인 | P10-P12 stage release |

본품 고가 부품(screw/barrel/die, 나머지 cutter)은 coupon 합격 전에 주문하지 않는다. 현재 기술 gate PASS는 이 승인들을 대체하지 않는다. `physical_gate_status` 계열 상태는 구매·가공·통전 모두 false다.

## 6. 비용 현황 (정보 제공, 구매 승인 아님)

`bom/cash_budget.csv` 기준 신규 현금비용 목표 합계 176,076 KRW, 예비비 포함 상한 196,076 KRW이다. 이번 일괄 커밋에 포함된 BOM 변경은 가열기·센서 사양 변경을 반영한다(die heater: Tempco 맞춤 견적 대기 `QUOTE_EXCEEDS_PLANNING_BUCKET_EXPECTED_HOLD`, 가열 MOSFET 5ch -> 4ch). 4,000 KRW 등 일부 값은 견적이 아닌 계획 bucket이므로 실제 견적 수령 후 재산정해야 한다. 이 변경들은 미검토 입력으로 커밋되었으므로 구매 전에 사용자 검토가 필요하다 (INFERRED: 일괄 커밋 전 파일별 검토는 이번 세션에서 하지 않았다).

## 7. 실패 시 처리와 판정 권한

1. 실패한 구획과 그에 의존하는 후속 단계만 HOLD한다. 독립 작업은 계속한다.
2. 원시 데이터(사진·영상·CSV)와 정확한 구성을 SHA-256과 함께 보존한다.
3. 가장 이른 영향 P-stage를 찾아 CAD/BOM/전기/펌웨어 source-of-truth를 수정하고, 영향받는 디지털 검사와 release artifact를 재생성한 뒤 같은 실물로 재시험한다.
4. 합격 기준을 사후에 완화하지 않는다. 임의 가공·shim 변경도 설계 기록 대상이다.
5. 판정 권한: 설계·반증 에이전트는 PASS를 쓰지 않는다(IMPLEMENTED/BLOCKED/FAILED만). 최종 판정은 분석기 코드와 사람 리뷰어. 시험마다 기계·부품 ID, source commit, 가공·열처리 lot, 계측기·교정, 작업자·독립 검토자, 시간대 포함 시각, 원시 증거 경로와 SHA-256을 기록한다.

## 8. 안전 경계

- E-stop, lid/service interlock, thermal fuse, branch fuse는 소프트웨어에 의존하지 않는다. E-stop 버튼 보유는 K0 contactor, positive-opening 스위치, thermal cutoff 확보를 뜻하지 않는다.
- 회전체·히터·고전류의 물리 검증은 물리적 lockout과 사용자 확인 없이 완료로 표시하지 않는다. 첫 통전은 logic branch만 current-limited로 수행하고 motor/heater branch는 분리한다.
- donor 부품의 전압·전류·토크·축경·센서 형식은 추측하지 않고 라벨·사진·실측으로 확정한다.
- GGM 소프트웨어 torque limit 8.0 N.m, 기계식 보호 실측 목표 8.8-9.3 N.m(250 mm arm에서 35.2-37.2 N). 과거 Gate-1의 18/22/24 N.m 값은 현 설계의 합격 기준이 아니다.
- 고온부: PI 테이프 220 C는 판매자 주장 하한에서 정한 잠정값이며 검증된 연속 정격이 아니다. 직접 heater/barrel/die 감싸기와 안전장치 대체는 금지한다.

## 9. 미해결 입력 (공개 배포 차단이 아니라 결과가 달라질 실제 입력)

GGM donor/구매품 라벨·정격·serial·축/PCD/편심, 프레임 유효 stock 길이·kerf·실제 조립 외형(nominal 470x700x930에 대한 실측), screw/barrel의 동일 heat·Q&T·질화·후가공 경로(JLCCNC 회신은 현 사양 전체 공정을 충족하지 않음, P5 전 본품 발주 금지), 보호 핀 lot별 파단 torque 분포, 고온부 열간 fit·잔류 예압·누설, PI 테이프 제조사·lot·같은 롤 coupon, 전기 DC 차단 정격·PE·절연·interlock, 측경·권취 교정, 수명·인증. 상세는 `docs/final/open_items_ko.md`.

## 10. 사용자 결정 체크리스트

- [ ] P1 재고 조사 착수 (승인 불필요, 담당자 지정)
- [ ] GGM 모터 2세트 구매 승인(S2) 또는 재고 대체 여부
- [ ] 6절의 BOM 변경(Tempco 맞춤 heater, 4ch MOSFET)과 예산 변경 검토
- [ ] 이번 세션에서 생성한 미커밋 정본 증거 4개(compliance 등)의 커밋 시점과 ZIP 재생성
- [ ] COMPLETE ZIP 재생성과 GitHub Release 게시 범위
- [ ] 연결 도달성 검사(WP-1), 연속 최소 거리 하한(WP-2) 등 L1/L2 오라클 보강 여부 (PROPOSED, 미구현)

## 부록 A. 단계별 계약 원문 (`validation/physical_v08/physical_gate_contract.json`)

아래는 계약 파일에서 자동 발췌한 선행 조건과 합격 기준이다. 이 문서의 요약보다 계약 파일이 우선한다.

### P0 DIGITAL_TECHNICAL_ENTRY

- 작업: record-only
- 합격 기준(계약 원문):
  - 23/23 technical digital gates PASS
  - release ZIP and remote policy explicitly excluded from this entry decision
- 해제 대상: P1 planning and user-approved stock/receipt inspection only

### P1 INVENTORY_AND_RECEIPT

- 작업: unpowered inspection
- 선행 조건:
  - P0 PASS
  - explicit user approval before any purchase
- 합격 기준(계약 원문):
  - selected GGM motor/gearbox receipt dimensions within inspection packet intervals
  - profile usable lengths reconciled to active cut list
  - bearing/heater/sensor/safety component identities recorded
  - owned assets distinguished from physically inspected assets
  - TH-INS-01 exact identity/backing/adhesive/dimensions/continuous service rating recorded before installation
- 해제 대상: final mount drilling dimensions; P2 cold fabrication

### P2 COLD_FRAME_AND_FIT

- 작업: cut/print/assemble without electrical power
- 선행 조건:
  - P1_RECORD_CHECK_PASS from exact 30-item inventory plus authenticated GGM receipt packet
  - GGM mount result AS_DRAWN_COMPATIBLE_NOT_AUTHORIZED against current design binding
  - 2020 and 2040 stock nesting PASS from measured length minus U95 and approved kerf budget
  - P2 bound fabrication approval matches exact P1 inventory, GGM packet, profile stock, current frame cut list and kerf budget
  - P2 approval does not authorize procurement or energization
- 합격 기준(계약 원문):
  - frame base 470 +/-0.8 x 700 +/-0.8 mm under FR-001 ISO 2768-m general tolerance; full U95 interval inside limits
  - frame diagonal difference plus both diagonal U95 contributions <=1.0 mm and no rocking
  - rail squareness <=0.50/700 mm including U95
  - 2020/2040 cut lengths checked before cutting
  - rotating-to-static shredder clearance >=1.90 mm
  - extruder cold axial travel >=1.50 mm
  - guards/covers fit without entering moving or hot envelopes
- 해제 대상: P3 drive bench fixture; P5 process coupons

### P3 GGM_DRIVE_BENCH

- 작업: guarded low-voltage motor bench test, no cutter/screw/heater load
- 선행 조건:
  - P0 PASS
  - P2_STAGE_RELEASE_VALIDATED against the same GGM receipt packet used for P3
  - GGM receipt/mount compatibility remains AS_DRAWN_COMPATIBLE_NOT_AUTHORIZED
  - BTS7960 wiring checked
  - current sensor identity/wiring verified; independent current reference available for in-gate calibration
  - P3 pre-power evidence record check PASS; this does not itself authorize energization
  - user explicitly approves energization for the P3 fixture after reviewing the preflight evidence
- 합격 기준(계약 원문):
  - SH K9G75C and EX K9G150C no-load speed/current recorded
  - current calibration error including U95 <=0.10 A over useful range through at least 4.6 A
  - current-to-output-torque holdout error <=0.40 N.m
  - software gearbox torque limit 8.0 N.m remains below mechanical release target
  - mechanical protection coupons release 8.8-9.3 N.m; SH forward/reverse and EX forward each >=3 independent coupons
  - extruder reverse remains prohibited
- 해제 대상: P4 powered shredder coupon; P6 extruder drive installation

### P4 SHREDDER_COUPON

- 작업: two-cutter guarded coupon only
- 선행 조건:
  - P3 PASS
  - CUT-01 quantity exactly 2
  - guard/interlock/hard cut verified
  - user approval for Gate-1 coupon
- 합격 기준(계약 원문):
  - each assembled sprocket radial TIR including U95 <=0.10 mm and total axial shift including U95 <=0.20 mm
  - 12T/30T key flank carries torque and received maker retention hardware provides axial retention only
  - direct-keyed GGM_SH_12T and GGM_SH_30T are used; DRV-02 is not an active P4 part
  - no permanent shaft/plate/guard damage
  - no repeated software torque-limit operation during representative normal PLA/PET body feed
  - bounded reverse recovery works without automatic restart
  - after at most one recirculation: 3-6 mm mass fraction >=70%, >20 mm PET strip <=2%, fines <=15%, mass recovery >=95%
  - actual torque/current/RPM curves recorded; old 22/24 N.m acceptance values are not used
- 해제 대상: remaining CUT-01 quantity may be considered for fabrication; P5/P6 continue

### P5 SCREW_BARREL_PROCESS_COUPON

- 작업: supplier/process coupons only
- 선행 조건:
  - P0 PASS
  - user approval for EX-CPN-SCR and EX-CPN-BAR only
- 합격 기준(계약 원문):
  - EX-CPN-SCR L48.00 +/-0.05 mm, pitch 16.00 +/-0.03 mm, flight OD 15.90-15.92 mm, root OD 10.88 +/-0.03 mm, land 1.60 +/-0.05 mm
  - EX-CPN-BAR L60.00 +/-0.05 mm, OD 34.00 +/-0.05 mm, final ID 16.20 +0.02/0 mm
  - matched actual diametral clearance including measurement uncertainty remains 0.28-0.32 mm at 18-22 C
  - Q&T core hardness 28-32 HRC; screw surface hardness 900-1100 HV0.3; barrel surface hardness >=900 HV0.3
  - screw effective case after final grind 0.30-0.50 mm
  - barrel nitride process target 0.30-0.50 mm is recorded and effective case after final hone is >=0.25 mm; final hone removal is recorded
  - screw flight OD Ra <=0.8 um and root/flank Ra <=1.6 um; barrel bore Ra 0.4-0.8 um
  - SCM440/JIS G4105 material/heat, Q&T/nitriding/final-finish route, inspection and subcontractor responsibility are traceable
  - baseline SCM440 245-270 C properties are collected if available but are not a standalone P5 blocker; any material/heat-treatment deviation requires property evidence and engineering re-analysis
- 해제 대상: full EX-SCR-01/EX-BAR-01 quotation/order may be considered, still requiring explicit user approval

### P6 COLD_EXTRUDER_ASSEMBLY

- 작업: full mechanical dry assembly, heater power disconnected
- 선행 조건:
  - P5_STAGE_RELEASE_VALIDATED for qualified screw/barrel process route and heat reservations
  - full production screw/barrel receipt inspection PASS against the exact P5 route/heat reservations
  - P3_STAGE_RELEASE_VALIDATED with p6_entry_prerequisite=true for the calibrated extruder GGM drive
  - P3/P5 release semantics remain fail-closed; neither release authorizes P6 energization
- 합격 기준(계약 원문):
  - hand rotation through full screw travel without rub/bind
  - screw/barrel diametral clearance 0.28-0.32 mm from supplier/receipt evidence
  - 51102 pocket diametral clearance 0.30-0.35 mm
  - loaded-direction thrust endplay 0.05-0.15 mm
  - drive coaxiality <=0.05 mm
  - front guide available cold axial travel >=1.50 mm
  - rear retainer cold endplay 0.12-0.28 mm
- 해제 대상: P7 electrical integration

### P7 ELECTRICAL_SAFETY_AND_LOGIC

- 작업: logic-only/current-limited commissioning before motor/heater branches
- 선행 조건:
  - mechanical guards fitted
  - K0/hardwired chain and branch protection physically present
  - user logic-power approval
- 합격 기준(계약 원문):
  - PE bond <=0.10 ohm at each required metal bond
  - insulation check passes applicable isolated circuit test without exposing electronics to inappropriate megger voltage
  - 24 V rail 22.8-25.2 V under logic-only check
  - logic startup current <=0.5 A
  - opening E-stop/lid/service or either TF-BARREL/TF-DIE series terminal removes K0 coil energy
  - reset never creates automatic motor/heater command
  - all fuse IDs and point-to-point wiring match schedule
- 해제 대상: P8 installed motor dry-run

### P8 INSTALLED_MOTOR_DRY_RUN

- 작업: one motor branch at a time, heaters disabled, no plastic
- 선행 조건:
  - P3_STAGE_RELEASE_VALIDATED for the installed GGM calibration basis
  - P6_STAGE_RELEASE_VALIDATED for cold extruder assembly
  - P7_STAGE_RELEASE_VALIDATED for logic/safety wiring
  - FIRMWARE_COMMISSIONING_RECORD_CHECK_PASS for applied P3 profile, final HEX, flash readback, GGM_REPORT and tach PPR
  - guards closed and heater branches isolated
  - explicit user motor-power approval recorded for this P8 run
- 합격 기준(계약 원문):
  - shredder cutter speed near design 16 rpm after chain ratio, actual value recorded
  - screw starts at <=10 rpm for commissioning and never exceeds 20 rpm hard limit
  - bearing/coupling temperature rise and vibration show no abnormal trend during bounded dry run
  - stop/E-stop/tach-loss behavior verified without automatic restart
  - one motor branch energized at a time during first dry-run sequence
  - GGM shredder/extruder measured current including U95 remains <=6.0 A
- 해제 대상: P9 empty-hot-zone entry review only; heater power remains separately approved

### P9 EMPTY_HOT_ZONE

- 작업: empty guarded hot-path thermal commissioning; motors inhibited
- 선행 조건:
  - P7_STAGE_RELEASE_VALIDATED for electrical safety/logic
  - P8_STAGE_RELEASE_VALIDATED for installed motor dry-run state
  - HOT_ZONE_RECEIPT_RECORD_CHECK_PASS against current thermal contracts
  - THERMAL_CUTOFF_TOPOLOGY_PASS: TF-BARREL then TF-DIE in K0 coil chain
  - TH-INS-01 receipt identity and S4 coupon smoke evidence PASS under thermal barrier tape contract
  - metal hot shield and remote stop available
  - explicit user heater-power approval recorded for this bounded P9 run
- 합격 기준(계약 원문):
  - T1-T5 mapping verified and sensor open/short faults detected
  - PLA and PET target temperature means remain within +/-5 C including U95
  - run peak + U95 remains below generated firmware overtemperature ceiling
  - polymer leak-tightness is NOT evaluated in the empty-path test; post-cycle insulation/PE remains valid
  - hot-zone does not bottom axial allowance; cold available travel was >=1.50 mm
  - forced-open TF-BARREL and TF-DIE each independently remove K0/heater energy
  - M4 die fasteners are 42.5 +/-0.1 mm from M4x45 class10.9 stock and installed dry at 1.50 N.m after receipt checks
  - thermocouple retainer remains <=0.10 mm motion after hot-cycle 20 N pull check
  - TH-INS-01 installed only on allowed grounded hot-shield exterior surfaces; it does not cover heaters/cutoffs/probes/terminals/vents
  - TH-INS-01 adhesive-interface peak + U95 + 30 C <= documented continuous service rating; cooldown edge lift + U95 <=2.0 mm and no smoke/char/melt/adhesive flow
- 해제 대상: P10 low-feed PLA

### P10 PLA_LOW_FEED

- 작업: first material process validation
- 선행 조건:
  - P4_STAGE_RELEASE_VALIDATED for shredder coupon configuration
  - P6_STAGE_RELEASE_VALIDATED for production screw/barrel cold fit
  - P8_STAGE_RELEASE_VALIDATED for installed motor dry-run state
  - P9_STAGE_RELEASE_VALIDATED for empty hot-zone thermal state
  - known dry PLA lot with authenticated drying evidence
  - explicit user material-feed approval for this bounded P10 run
- 합격 기준(계약 원문):
  - start screw around 8-10 rpm and increase only from measured torque/diameter behavior
  - no leak, uncontrolled pressure symptom, guard contact, or repeated torque trip
  - 20 consecutive stable diameter samples: mean error <=0.05 mm, ovality <=0.05 mm, U95 <=0.03 mm target
  - actual mass/time, temperature, screw RPM, current/torque, puller RPM recorded
- 해제 대상: P11 PET test

### P11 PET_LOW_FEED

- 작업: dry PET process validation after PLA succeeds
- 선행 조건:
  - P10_STAGE_RELEASE_VALIDATED for bounded PLA material-run state
  - known cleaned/dried PET lot with authenticated drying evidence
  - PET thermal profile bound to current generated firmware targets
  - explicit user PET-feed approval for this bounded P11 run
- 합격 기준(계약 원문):
  - start screw around 8-10 rpm; higher speed is approached only from measured torque/current/diameter behavior
  - all stable samples keep gearbox torque + U95 < 8.0 N.m and GGM motor current + U95 <=6.0 A
  - no leakage, uncontrolled pressure symptom, guard contact, repeated torque-trip control, or hot-zone binding
  - 20 consecutive stable diameter samples: mean error <=0.05 mm, ovality <=0.05 mm, U95 <=0.03 mm target
  - actual maximum stable throughput is reported instead of forcing 200 g/h
- 해제 대상: P12 forming/spool validation

### P12 FORMING_AND_SPOOL

- 작업: full strand path and spool validation
- 선행 조건:
  - P11_STAGE_RELEASE_VALIDATED with released PET lot identity
  - gauge/puller/dancer/traverse calibration evidence authenticated
  - explicit user full-path approval with P12_FULL_PATH_RUN scope
- 합격 기준(계약 원문):
  - P12 source_lot_id exactly matches the released P11 PET lot
  - puller slip + U95 <=1% during stable interval
  - traverse usable width - U95 >=68 mm and no end collision or jam
  - dancer controlled-stop angle + U95 <0.36 rad and peak + U95 <0.4363 rad hard stop
  - 1 kg nominal winding path completes without spill, guard contact, leak or pressure symptom
  - diameter mean error/ovality remain <=0.05 mm with diameter U95 <=0.03 mm
  - gearbox torque + U95 <8.0 N.m and GGM motor current + U95 <=6.0 A
- 해제 대상: physical-validation evidence package may be reviewed; not automatic production/safety certification

