# T1–T4 프로브 구매 기준 — Tempco MTA1 맞춤품 / 승인도면 HOLD

2026-09-08 공식 MTA1/MI cable 자료를 확인해 `TH-TC-01` 디지털 기준을
Type-K, ungrounded, Alloy600 `Ø3.00±0.03`, 25.40 mm sheath, 고온 potting/
fiberglass lead와 공급자 용접 stop collar로 고정했다. 상세 치수·retainer·수령시험은
`docs/final/thermocouple_selection_basis_ko.md`가 지배한다. 아래 AliExpress 조사는
역사적 대체후보 기록이며 판매자 회신 전에는 기준품을 대체하지 않는다.

추가 조사: 한국어 AliExpress 원문도 접근 실패했다. 보조 목록의 제목/가격을
판매자 보증 사양으로 승격하지 않는다.

2026-09-08 재조회에서는 다음 판매 식별자의 최신 보조 목록을 확인했다.

- [1005010610023805](https://www.aliexpress.com/item/1005010610023805.html):
  WRNK-191 K형, Ø3/4 mm, 100/200/300/500 mm, 0–1100°C라는 목록 제목과
  2026-08-29 갱신 가격 US$7.50만 확인했다.
- [1005004874800021](https://www.aliexpress.com/item/1005004874800021.html):
  K형/PT100, ungrounded, Ø1/2/3/5 mm 선택지라는 목록 제목과 2026-08-25
  갱신 가격 US$2.77만 확인했다.
- [1005004962533904](https://www.aliexpress.com/item/1005004962533904.html):
  M8 spring 형식, 50/100/150/200 mm 선택지라는 목록 제목과 2026-07-22
  갱신 가격 US$2.48만 확인했다.

가격은 배송·세금·선택 옵션을 확정한 견적이 아니다. 세 상품 모두 원본 치수도와
SKU별 외경 공차, 접점 위치, 최소 삽입, 전이부 정격 및 고정 하중 자료가 없어
T1–T3 승인 MPN으로 선정하지 않았다. 특히 100 mm 이상 sheath와 M8 spring은
현재 5.15–5.25 mm 삽입 후보에 그대로 적용할 근거가 없다. 주문 수량은 0이다.

## 열접촉 조건

재실행 시작 시 요약의 solver 상태를INCOMPLETE로 저장해 이전 PASS를 무효화한다.
실행 파일 누락/timeout은FAIL과 예외 종류를 기록하고, timeout의 부분 출력도
해당 원시 폴더의 solver.log에 남긴다. 그 밖의 결과 파싱 실패는INCOMPLETE로
남아 PASS로 사용될 수 없다. 임시 디렉터리에 과거 PASS를 주입한 뒤 실행 파일
누락과 timeout을 각각 재현하는2개 회귀시험 및 실제3개 시나리오 재실행이 통과했다.

시간영역 검사를 보강했다. 기존에는 마지막 시각120초와 행 수만 확인하여
동일한 마지막 샘플을 반복한 CSV도 통과할 수 있었다. 이제0초 시작/120초 종료,
서로 다른 시각1201개 이상, 역행 없음, 최대 간격0.100001초, 유한 온도 및
해석해 오차<1e−4°C를 함께 요구한다. `validation/test_probe_thermal_evidence.py`의
누락·중복·역행·NaN·오답 등8개 음성 사례를 거부했고 실제 OpenModelica3개
시나리오도 재실행해 통과했다. 이는 시간영역 증거의 완전성 검사이며 제품 검증이 아니다.

`analysis/final_validation/input/ProbeThermalContact.mo`로 별도 단일 접점 과도응답
모델을 만들고 OpenModelica1.27.0에서3개 열접촉 가정으로120초씩 실행했다.
전1201개 이상 시점의 해석해와 차이<1e−4°C 및 정상상태 열수지를 검사한다.
실행은 `probe_thermal_screen.py <omc 경로>`이며 Nix판 omc에는 동일한 고정
nixpkgs의 gcc/binutils wrapper를 PATH 앞에 둔다. 기본 시스템 clang과 혼합하면
GLIBC ABI 오류가 발생했다. 실패 로그도 원시 폴더에 보존했다.
C 컴파일러는 [공식 setCompiler API](https://build.openmodelica.org/Documentation/OpenModelica.Scripting.setCompiler.html)로 지정했다.
기존 v0.8 온도60초 시정수 모델은 센서 모델이 아니므로 이 검증과 구분한다.
모델 일치는 구매품의 열컨덕턴스·열용량·정확도 인증이 아니며 제품 HOLD는 유지한다.

구매 후보의 삽입 깊이 적합성은 별도 확인해야 한다.
[Omega ADR/ADF 공식 자료](https://www.dwyeromega.com/en-us/adjustable-depth-armored-thermocouples/p/ADR-ADF-PROBES)
는 자체 제품에 최소 삽입70 mm 및 스프링으로 well 바닥에 접촉하는 구조를 제시한다.
이는 해당 제품의 조건이며 AliExpress 후보에70 mm를 그대로 적용하지 않는다.
해당 Omega 제품은 현재5.2 mm 삽입용 대체품으로 선정하지 않았다.

`python3 analysis/final_validation/probe_thermal_screen.py`는
Gc(Twall−Tj)=Gs(Tj−Tambient)의 단일 접점 정상상태 모델을 검사한다.
wall270°C/ambient25°C에서 예시 편차1/2/5/10°C를 만족하려면
접촉/스템 열컨덕턴스 비Gc/Gs가 각각244/121.5/48/23.5 이상이어야 한다.
이는 예시 오차 예산이며 실제 시스템 합격기준이나 구매품 성능이 아니다.
현재 바닥 여유0.10–0.30 mm 후보는 끝단 접촉을 보장하지 않는다. 측면 접촉,
열접촉재의 온도/전기절연 적합성, stem 손실과 과도응답 근거가 필요하다.

사용자 확인: 실제 프로브는 미선정이며 AliExpress 제품 조사·선정은 허용됨.
2026-09-08 사용자가 후보 상품 판매자에게 문의를 전송했다고 확인했다. 답변과
첨부자료는 아직 수신하지 않았고 주문·결제는 실행하지 않았다. 기존 BOM 승인 MPN은
변경하지 않는다.

## 조사 후보

### 짧은 카트리지 대체 검토 후보: Slice Engineering Type K

[제품에서 연결한 설치 지침](https://support.sliceengineering.com/portal/en/kb/articles/article-1-3-2021)은
센서보다 긴 hot-block 슬롯의 빈 공간을 dowel pin으로 채우고, 양 끝 retaining
screw와 boron nitride paste를 사용하는 구성을 설명한다. 이것은 현재 배럴의
짧은 blind bore에5.2 mm만 삽입하는 방식의 승인 근거가 아니다. 원래 슬롯용
핀을 blind bore 바닥에 추가하면 삽입 공간을 더 줄이므로 그대로 전용하지 않는다.
따라서 선정 전 확인 질문을 “5.2 mm 부분 삽입에서의 접점 위치·허용 설치 오차·
열응답과 외부 금속 고정 방식”으로 구체화한다. 열전도 페이스트가 있다는 사실만으로
측정 정확도나 인발 방지가 확보된다고 취급하지 않는다. 제조사에 문의를 발송하지 않았다.

AliExpress의 짧은 sheath 검색에서는 검증 가능한 판매 원문을 확보하지 못했다.
대신 [제조사 공식 제품 페이지](https://www.sliceengineering.com/products/thermocouple)에서
ungrounded K형, 카트리지 Ø3×15 mm, 2 m bare lead, 온도 한계400°C와
정확도 표기±2.2°C 또는±0.75%를 확인했다. 이는 AliExpress 제품이 아닌 비교 후보이며
승인 MPN이나 주문으로 전환하지 않았다. 현재 후보 삽입5.2 mm를 적용하면
카트리지의 명목 외부 길이는15−5.2=9.8 mm다. 이 산술값은 고정 여유나
최소 삽입 적합성을 입증하지 않는다.

이 제품은 기존 RND150 mm보다 짧은 실재 외형을 제공하므로 다음 CAD 비교에
사용할 수 있다. 다만 외경 공차, 선단 내부 접점 위치, 5.2 mm 삽입에서의
정확도/응답, 전이부 온도 한계 및 고정 조건은 확인되지 않았다. 특히 제품의
정확도 표기를 현재 배럴 설치 상태의 총 오차로 적용하지 않는다.

### 원본 사양을 확보한 대체 검토 후보: RND 410-00143

[Distrelec/RND 공식1쪽 데이터시트](https://media.distrelec.com/Web/Downloads/_t/ds/RND_410-00143_eng_tds.pdf)
에서 K형, nominalØ3 mm, sheath150 mm, SS310, sheath로부터 절연된 접점,
Class1 표기,1 m PFA 리드를 확인했다. Plain pot seal은200°C로 명시되어
있으므로 배럴270°C와 같은 온도로 노출시키면 안 된다. 문서의1100°C 표기를
전이부·리드·전체 조립체의 허용 온도로 적용하지 않는다.

이는 AliExpress 제품이 아닌 비교용 대체 후보다. 재고·가격·배송은 확인하지
않았으며 주문이나 승인 MPN 변경은 없다. Ø3의 외경 공차, 선단과 접점 위치,
최소 삽입 깊이, pot의 외경/길이,5.2 mm 삽입에서의 오차·응답은 이1쪽 자료로
확정할 수 없다. 따라서 기존Ø3.05 mm 최대 외경 가정도 대체하지 않는다.
PDF 텍스트 원문은 확인했으나 페이지 이미지 확인은 timeout으로 실패했다.
구조화 IC extraction cache는 생성하지 않았으며 공개 PDF의 부품 사양과
누락값만 수동 대조했다. 디지털 후보 선정 상태는 여전히 HOLD다.

추가 AliExpress 후보1005010610023805와32655524562는 보조 검색 목록에서
발견했으나 판매 원문 열기가 non-retryable error로 실패했다. 후보 수를 늘려도
판매자 보증 사양이 확보된 것은 아니므로 기존 미선정 판단을 유지한다.

- [AliExpress 상품1005004874800021](https://www.aliexpress.com/item/1005004874800021.html)
- [발견 경로: Pricearchive 상품 기록](https://www.pricearchive.org/aliexpress.com/item/1005004874800021)

보조 목록 제목에 K형/PT100, ungrounded, 1/2/3/5 mm 옵션이 함께 표시된다.
이는 SKU별 사양 검증이 아니다. 판매 원문 열기는 실패했고, 원본 치수도/PDF를
확보하지 못했다. 따라서 재고·가격·배송·판매자·옵션·적합성은 미확정이다.
AliExpress1005004962533904도 검색되었으나 M8 spring 형식의 외형 및 절연 접점이
확인되지 않아 우선 후보로 채택하지 않았다.

## 확인할 구매 옵션 및 자료

1. K형, 접점과 금속 sheath가 절연된 ungrounded 구조. PT100/J형 선택 금지.
2. nominalØ3 mm의 실제 최대 외경. 현재 간섭 계산용 상한은Ø3.05 mm이나 구매품 보증값이 아님.
3. sheath 전체 길이, 선단 형상/접점 위치, 최소 삽입 길이, 전이부 외경 및 길이.
4. sheath·전이부·리드 각각의 연속 사용 온도와 절연 사양. 상품 제목의 최고 온도를 전체 부품에 적용하지 않음.
5. 조정 가능한 금속 고정 방식 및 인발/진동 유지 조건. 판매 치수도와 CAD 외형 대조 필요.

현재 후보 보어5.40±0.05 mm 및 삽입5.20±0.05 mm는 아직 출시 설계가 아니다.
구매품의 긴 sheath를 임의 절단하거나 단순히 짧은 삽입으로 온도 정확도가 확보된다고
가정하지 않는다. 가이드 축 정렬·열응답·수령 절연/교정 검증 후에만 승인 MPN으로 승격한다.
