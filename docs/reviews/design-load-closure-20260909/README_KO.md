# v0.8 고온부·하중 경로 직접 보완 — 2026-09-09

이 기록은 실제 mathcat 머신에서 수행한 코드 수정, FreeCAD 형상 검사와 CalculiX 실행 기록이다. 전체 기계 제작 승인 문서가 아니다.

## 실제 원본 변경
- `geometry.py`: CUT-05R의 키홈을 독립 정의했다. 오른쪽 축의 local Y57–69 및 Y197–209 베어링 좌면에 기존 공통 키홈이 지나가던 문제를 제거했다.
- CUT-05R cutter keyseat는 Y85–165, phase keyseat는 Y212–240이다. drive Y0–35, 직경·길이·각도 기준은 유지했다.
- 조립체, 제조 지그와 clocking 검증에서 좌·우 shaft variant를 명시한다.
- `final_v08/generate.py`: collar의 bore/length/location이 실제 파라미터를 따르게 수정했다. 기본값에서 고온부 형상 5개의 대칭차 체적은 0이었다.
- 후방 support rail의 잘못된 L430 라벨을 실제 파라미터 L390으로 연결했다.

## 계산 범위
- 실제 keyed STEP을 C3D4로 해석한다. chain은 실제 CAD처럼 motor 쪽 +Z로 당기며 gear의 작용·반작용과 양축의 반대 회전을 반영한다.
- 분포 하중은 지정한 힘 3성분과 모멘트 3성분을 동시에 보존한다. bearing은 가중 강체운동 투영으로 병진만 구속하고 회전은 자유롭게 둔다.
- 정·역전, 두 축의 토크 분담 극한, 3단계 메시를 포함한다. 22 N·m는 기존 기계식 fuse 사례다.
- slack tension 60 N, hook 유효 반경18 mm, 추가 radial wedge force 미정 상태는 가정으로 남긴다. 이를 실제 최대 하중이라고 주장하지 않는다.
- 제조사 SCM440 일반표의 CTE12.3e-6/K를 참고값으로 기록했다. 17e-6/K는 기존 screening 상한 가정이지 실측 물성이 아니다.
- 실제 고온부 BRep를 barrel270/300°C, support20/100/200°C 조건으로 팽창시켜 접촉을 검사했다. 이는 온도장/접촉응력 해석을 대체하지 않는다.

## 판정 경계
- 원형 journal 확보, 키 결합 위치, STEP solid 재수입과 지정 load resultant/변위 수렴은 범위를 한정해 판정한다.
- 고온부의 일부 자유팽창 조합에서 간섭이 발생했다. 간섭 체적만으로 실제 항복·고착을 확정하지 않지만, 자유 sliding을 무조건 가정할 수도 없다.
- 구멍을 임의로 크게 만들지 않았다. screw/barrel 중심 정렬과 thrust 경로를 함께 검증해야 한다.
- 고온 물성, 온도/접촉 경계, gasket seating/잔류 예압 및 추가 jam force의 근거가 없으므로 전체 제작 상태는 HOLD다.
- 기존 FABRICATION ZIP은 갱신·승인하지 않는다. 새 파일은 `exports/review/engineering-closure-20260909/`의 검토용 자료와 구분한다.
