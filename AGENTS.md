# Filament Recycler Agent Rules

이 저장소의 모든 작업은 아래 규칙을 따른다. 루트의 지시는 하위 디렉터리 전체에 적용된다.

## 소유권과 언어

- parent Codex가 최종 요구사항, 아키텍처, 안전 결정, 외부 저장소, merge, release acceptance를 소유한다.
- 사용자 보고와 프로젝트 핵심 문서는 한국어로 작성한다. 코드 식별자와 표준 용어는 영어를 병기할 수 있다.
- 실행 요청은 계획에서 멈추지 않고 요청 범위의 파일과 필요한 검증 결과를 남긴다. 읽기 전용 검토는 인용과 제안이 산출물이며 파일 생성을 요구하지 않는다. 미완료 항목은 완료로 표시하지 않는다.
- 시뮬레이션 결과와 실제 물리 시험 결과를 명확히 구분한다.

## 자율성·명확화·승인

- parent의 소유권은 검토·조정 책임이며 사용자 승인 요구를 대체하지 않는다.
- 사용자 요청에 포함된 일상적인 로컬 수정·계산·검증은 추가 확인 없이 완료한다. 동일 대상·범위·조건의 기존 승인은 재사용하되, 별도 승인이 필요한 물리 단계에는 전용하지 않는다.
- 불명확한 사항은 먼저 기존 문서와 증거로 해소한다. 안전·정격·구매 대상·비용·외부 공개 범위를 결정할 정보가 부족하면 해당 결정만 보류하고 독립 작업을 계속한다. 필요한 질문은 묶어서 요청한다.
- 현재 revision의 상태와 정책 진입점은 `docs/final/release_notes_v1.0.0-rc1_ko.md`다. 과거 revision의 계약·보고서는 역사 기록이며 이후 작업에 자동 적용하지 않는다. 현재 HOLD, 제작 승인, merge·게시 제한은 별도로 유지한다.
- Skill의 절차는 요청 범위와 기존 승인을 따른다. API 키 존재는 비용 승인이나 외부 공개 승인이 아니다.

## 로컬 subagent

- 비밀값은 루트 `.env`의 `KOTORI_SUBAGENT_API_KEY`에서만 읽으며 출력, URL, 로그, 예외, 저장소, 커밋에 남기지 않는다.
- `.env`의 `SUB_ENDPOINT`는 현재 스킴 없이 `/v1`을 포함한다. 호출 시 메모리 안에서만 `https://`를 앞에 붙이고 중복 `/v1`을 만들지 않는다.
- 첫 사용 전 `/v1/models`, `/v1/responses` 의미 시험, harmless tool-call probe를 수행한다.
- 확인된 모델 중 기본은 `dgx-moa-fast`, 높은 정확도·성능이 필요한 독립 계산 검토만 `dgx-moa`를 사용한다.
- subagent에는 파일 경계와 합격 기준이 분명한 작업만 맡긴다. 같은 파일에 여러 writer를 동시에 배정하지 않는다.
- subagent는 원격 저장소 생성, push, 구매, 가공 승인, 최종 안전 판정, merge를 수행하지 않는다.
- parent는 결과를 그대로 채택하지 않고 수식, 출처, diff, 실행 결과를 재검증한다.
- API timeout이나 불완전 응답은 결과로 채택하지 않는다. 진행을 막지 말고 parent가 직접 수행하며 실패를 기록한다.

## 안전과 구매

- E-stop, lid/service interlock, thermal fuse와 branch fuse는 소프트웨어 하나에 의존하지 않는다.
- cutter, screw, heater, mains/high-current의 물리 검증은 물리적 lockout과 사용자 확인 없이 완료로 표시하지 않는다. 디지털 구현·계산·시뮬레이션은 명시한 범위에서 별도로 완료 판정할 수 있으나 물리 검증·제작·운전 승인을 대체하지 않는다.
- 사용자 승인 없이 부품 주문, CNC 주문 또는 비용 지출을 진행하지 않는다.
- donor 부품 전압, 전류, 토크, 축경, 센서 형식을 추측하지 않는다. 사진, 라벨, 실측으로 확정한다.

## 설계와 검증

- 핵심 CAD의 source of truth는 FreeCAD Python과 파라미터 파일이다.
- 고하중 경로는 `metal part -> bearing/plate -> aluminum profile -> table`로 구성하고 출력물만으로 지지하지 않는다.
- 3D 출력 부품 기본 bounding box는 각 축 210 mm 이하로 제한한다.
- 실제 시험 전 계산값에는 가정, 경계조건, 안전계수와 검증 필요 상태를 붙인다.
- cutter/blade clearance는 출력 공차가 아니라 금속 shim으로 조절한다.
- 의미 있는 테스트만 작성하며 보호 요구사항, 의사결정 가치, 입력, 방법, 증거, 합격기준, 결과를 기록한다.

## Git과 산출물

- source of truth와 사람이 검토할 수 있는 경량 산출물은 추적한다. 재생성 가능한 큰 출력은 manifest와 생성 명령을 우선한다.
- 커밋 전 관련 생성 스크립트와 검증을 실행한다.
- `.env`, API 키, 인증 토큰, 다운로드 캐시, 주문용 임시 파일은 커밋하지 않는다.
- software/firmware/scripts는 MIT, hardware CAD/drawing/electronics는 CERN-OHL-P-2.0을 적용한다. 자세한 범위는 `docs/licensing.md`를 따른다.

## 지식 그래프 (graphify)

- 프로젝트 지식 그래프는 `graphify`로 구축한다. 소스: 코드(AST, 무비용) + 문서/도면/이미지(시맨틱 추출).
- 산출물 위치: `graphify-out/` — `GRAPH_REPORT.md`(보고서), `graph.json`(GraphRAG용), `graph.html`(인터랙티브 뷰), `manifest.json`/`cost.json`(증적).
- 추적 정책: `GRAPH_REPORT.md`, `manifest.json`, `cost.json`은 사람이 검토 가능한 경량 산출물로 추적한다. `graph.json`/`graph.html`/`cache/` 등 대용량 재생성물은 `.gitignore`로 제외하고 재생성 명령으로 복원한다.
- 실행: 전체 구축 `/graphify` Skill, 전체 코드·문서 증분 갱신 `/graphify --update` Skill (CLI `graphify update .`는 AST 갱신과 시맨틱 변경 감지만 수행), 조회 `graphify query "<질문>"` / `graphify path "<A>" "<B>"` / `graphify explain "<노드>"`. HTML은 5000 노드 초과 시 커뮤니티 집계 뷰로 자동 축소된다.
- 추출 기준: `EXTRACTED`(원문 명시), `INFERRED`(합리적 추론, 신뢰도 0.55–0.95), `AMBIGUOUS`(불확실, 0.1–0.3)로 구분해 감사 추적(audit trail)을 유지한다.
- 갱신 규칙: 문서/코드 변경 후 커밋 전 `/graphify --update` Skill로 코드·문서를 증분 반영하고, `GRAPH_REPORT.md`의 God Nodes / Surprising Connections / Suggested Questions를 검토한다. 명시된 범위는 파일 수만으로 재확인하지 않으며 증분 갱신은 변경 대상 규모를 기준으로 처리한다. 승인된 유료 실행 범위가 없으면 호스트 추출 등 추가 비용 없는 경로를 사용한다. 갱신 실패 시 원인을 기록하고 독립 작업을 계속하되, 필수 갱신 미완료 상태를 커밋 조건 충족으로 표시하지 않는다.
