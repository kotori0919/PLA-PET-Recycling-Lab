# v0.8 공급자 문의 패키지 — 발송·회신 기록

상태: 열전대 문의 `USER_REPORTED_SENT_AWAITING_RESPONSE` (2026-09-08) · JLCCNC 문의
`SENT_AND_REPLIED_2026-09-08` · 견적 수락: `NO` · 발주 승인: `NO` · 제작 승인: `HOLD`

현재 JLCCNC 첨부본: `dist/PPR-v0.8-JLCCNC-CAPABILITY-INQUIRY-DRAFT.zip`
(5 files, SHA-256 `2bd98319be7ae9aeea639ca12400b60c76ee0913100a9ca939e08cb6925753ed`).

JLC 부적합 회신 뒤 준비한 대체 전문업체 첨부본:
`dist/PPR-v0.8-SPECIALIST-HOT-ZONE-CAPABILITY-INQUIRY.zip`. 발송 전 후보와 근거는
`docs/final/hot_zone_alternative_supplier_shortlist_ko.md`를 따른다. 현재 상태는
`RFP_READY_NOT_SENT`이며 견적 수락·발주·제작 승인을 포함하지 않는다.
첨부본은 4 files, SHA-256
`83f5394521bf55a84b15c70c35628e1b67e50983335745cc3f7965820a211d07`이다.

이 패키지는 두 문의를 분리한다. JLCCNC에는 SCM440 가공·열처리·검사 능력을,
열전대 판매자에게는 실제 주문 SKU의 치수와 전기·열 사양을 묻는다. 모든 공급망 gate가 닫히기 전에는
대체재, 센서 홀 형상, 프로브 MPN 또는 생산품 가공을 승인하지 않는다.

## 1. JLCCNC 1차 문의

메일 초안: `docs/final/jlccnc_inquiry_email_en.txt`

권장 수신 경로: JLCCNC 계정의 공식 Contact/Live Chat 또는
`support@jlcpcb.com`. 공식 주문 안내에 표시되는 지원 주소가 페이지별로 다르게
렌더링되므로 실제 발송 직전 로그인한 Contact 화면에서 주소를 다시 확인한다.

첫 문의는 발송·회신이 완료됐다. 원본 판정과 인증 해시는
`docs/final/jlccnc_response_2026-09-08_ko.md`를 따른다.

### JLCCNC 회신표

공급자가 직접 채울 파일: `docs/final/jlccnc_capability_response.csv`

결과표는 `docs/final/jlccnc_capability_response.csv`에 있다. SCM440 조달, Q&T,
가스질화 및 coupon-first 순서는 `REJECTED`; 후처리 정밀가공, 센서 보어와 검사성적서는
개별 STEP 심사 조건부여서 현재 사양의 완결 공급처로 채택하지 않는다.

### 능력 확인 후 업로드할 파일

아래 파일은 현재 RFQ 디렉터리에서 가져온다. 이름을 바꾸거나 PDF와 STEP의 revision을
섞지 않는다.

| Part ID | 수량 | 파일 | 현재 gate |
|---|---:|---|---|
| EX-CPN-BAR | 1 | `exports/final/manufacturing/RFQ/EX-CPN-BAR.step`, `.dxf`, `.pdf` | coupon RFQ allowed |
| EX-CPN-SCR | 1 | `exports/final/manufacturing/RFQ/EX-CPN-SCR.step`, `.dxf`, `.pdf` | coupon RFQ allowed |
| EX-BAR-01 | 1 | `exports/final/manufacturing/RFQ/EX-BAR-01.step`, `.dxf`, `.pdf` | production HOLD |
| EX-SCR-01 | 1 | `exports/final/manufacturing/RFQ/EX-SCR-01.step`, `.dxf`, `.pdf` | production HOLD |

함께 보낼 문서:

- `docs/final/hot_zone_supplier_requirements_ko.md`
- `exports/final/manufacturing/RFQ/manifest.csv`에서 위 네 Part ID 행만 추출한 표
- 필요 시 전체 조립 맥락용 `docs/drawings/v0.8/EX-002_screw_barrel_die.pdf`

생산품은 coupon 결과 검토와 별도 사용자 승인 전 시작 금지라고 주문 메모에도 반복한다.
공급자가 45# steel, 4140 또는 다른 처리를 제안하면 동등하다는 표현만으로 승인하지 않고
정확한 규격·처리 상태·고온 물성을 받아 재해석한다.

## 2. 열전대 판매자 문의

메일/메시지 초안: `docs/final/thermocouple_supplier_inquiry_email_en.txt`

공급자가 직접 채울 파일: `docs/final/thermocouple_supplier_response.csv`

후보 상품마다 별도로 보내고 답변에 정확한 SKU/옵션을 적게 한다. 상품 제목이나 채팅의
“K type/1100°C” 답변만으로 선정하지 않는다. 반드시 치수도 또는 SKU별 데이터시트를 받는다.

### 열전대 회신표

| 확인 항목 | 공급자 값/파일 | 합격 조건 | 상태 |
|---|---|---|---|
| exact SKU/option |  | 답변과 주문 옵션이 일치 | HOLD |
| junction |  | metal sheath와 절연된 ungrounded | HOLD |
| sheath OD limits |  | nominal Ø3 및 실제 min/max 공차 제공 | HOLD |
| tip/junction geometry |  | 선단 형상·R·접점 위치 치수 제공 | HOLD |
| insertion |  | 약 5.2 mm 부분 삽입의 허용/오차/응답 근거 | HOLD |
| temperature ratings |  | sheath/transition/cable/connector를 분리 표기 | HOLD |
| electrical isolation |  | 절연저항과 시험전압 제공 | HOLD |
| retention |  | 금속 고정법과 pull/vibration 조건 제공 | HOLD |
| calibration |  | 적용 표준·accuracy class·성적서 범위 | HOLD |

사용자가 2026-09-08 후보 상품 판매자에게 문의를 전송했다고 확인했다. 회신 원문과
첨부자료는 아직 수신하지 않았다. 회신이 불완전하면 현재 `TH-TC-01`의 `UNSELECTED`를 유지한다. 구매 승인 후에도 수령품
외경 측정, sheath-to-junction 절연, 기준점 교정, 고정력과 열응답 시험은 별도다.

## 3. 대체 공급자 발송 전 체크

- 보내는 사람의 이름·국가·회신 이메일만 채운다.
- 첨부 파일 revision이 `final-design-fabrication-closure-v0.8`인지 확인한다.
- “capability inquiry only / not a purchase order” 문구를 삭제하지 않는다.
- 생산품 가격과 coupon 가격을 분리 요청한다.
- 공급자 대체안은 자동 수락하지 않는다.
- 회신 원문, 첨부 데이터시트, 날짜와 SKU/lot 연결을 그대로 보존한다.
- 회신을 받은 뒤 CAD/CalculiX/OpenModelica와 공차 gate를 다시 실행한다.

## 4. 실제 전송 순서

1. JLCCNC 회신은 완료됐으며 현 사양 후보에서 제외한다.
2. 대체 업체의 능력 확인 회신 후 coupon 2종의 STEP/PDF와 해당 manifest 행을 먼저 제출한다.
3. coupon 견적·성적서 범위가 수락된 뒤에만 생산품 STEP/PDF를 기술 검토용으로 제출한다.
4. 열전대 문의는 상품별 메시지로 보내고 `thermocouple_supplier_response.csv`와 치수도 요청을 붙인다.
5. 어떤 단계도 견적 수락·결제·생산 시작 승인을 포함하지 않는다.
