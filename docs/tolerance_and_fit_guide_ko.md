# v0.8 공차·끼워맞춤 검토 — PASS

단일 생성원 `calculations/tolerance_stack_final.py`, 지배 catalog `exports/final/interface_catalog.csv`.
`exports/fabrication/interface_catalog.csv`는 byte-identical compatibility mirror이며 별도 authority가 아니다.
임의 IF-01..16을 폐기하고 f3b1e66의 IF-001..032를 실제 원본과 대조했다. 중복 TS/IF는 추가 coverage가 아니다.
unknown은 JSON null/CSV 빈 수치다. 요구범위와 계산 결과를 분리하고 양쪽 한계를 검사한다.
전체 mating coverage: PASS. IF-030의 30개 unique joint contract와 assembly-step 1:1 참조를 함께 검사하며 단순 행 개수만으로 PASS하지 않는다.

PASS 48 / HOLD 0 / FAIL 0. 물리 NOT_RUN; 구매·제작·통전 USER_APPROVAL_REQUIRED.

## TS-01 — PASS

CUT-01 discs ↔ CUT-02 spacers/collars

- 원본 치수: numbered CUT-01/CUT-02 two-shaft matched stack; CAD stagger6.5
- 계산: match-grind/lap the numbered spacer set, shim with metal only, then accept every gap over one full hand rotation
- 결과: 0.25 … 0.5 mm / 요구: working gap 0.25–0.50 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:7` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/CUT-01/drawing_notes.md:8` SHA256 `951f419b6c5e4a0eec79ba69bbac37449e4aa406204c1b6dd7789b5a609ac629`
- 근거: `exports/cnc/CUT-02/drawing_notes.md:8` SHA256 `fc8793eda97780e80c31fec2e48331ec7c6f6fbfc7e07d98772c554488ebf5f4`
- 근거: `cad/freecad/compact/geometry.py:999` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`

## TS-02 — PASS

CUT-05 shafts ↔ CUT-03 matched plates

- 원본 치수: 0.125 axial float
- 계산: shim rear outer-ring retention, then accept each shaft directly by dial indicator over one full hand rotation
- 결과: 0.05 … 0.2 mm / 요구: 0.05 ≤ 0.125 axial float ≤ 0.2 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:28` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/CUT-05/drawing_notes.md:8` SHA256 `b8c1d480c8c503a81afc964e7ffc29643a6e3c1bfd2e5a5d3b7fa23c2eadb0fe`
- 근거: `exports/cnc/CUT-03/drawing_notes.md:8` SHA256 `474ab7438af4f1c656c03d16c1c0bddb7f8c4877009e0f36e4b32e1a7495368e`
- 근거: `exports/cnc/CUT-08/drawing_notes.md:8` SHA256 `6100cc12b6c1c0d950933735464ebacad69e3e983f938316b8cd797f9e1326a7`

## TS-03 — PASS

DRV-03/DRV-03R phase gears ↔ CUT-03 bearing centres

- 원본 치수: 48.00 centre / released pair
- 계산: released cold BRep pair ± CalculiX shaft/plate movement = 0.100681–0.159024; loaded backlash angle0.379642°; combined path0.903639°
- 결과: 0.100681 … 0.159024 mm / 요구: loaded backlash >0 and combined phase error ≤1° / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:49` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/CUT-03/drawing_notes.md:8` SHA256 `474ab7438af4f1c656c03d16c1c0bddb7f8c4877009e0f36e4b32e1a7495368e`
- 근거: `exports/drive_interface/parts/DRV-03/drawing_notes.md:7` SHA256 `29707f6e163aaa9bb2e1098af15feae1358b095d79e249b68d132c80bc1f1002`
- 근거: `exports/drive_interface/parts/DRV-03R/drawing_notes.md:7` SHA256 `eac6107619dd6f11a6c476590e0c580100b39cc264174d76e78bbbd057a5d0d0`
- 근거: `analysis/final_validation/results/v0.8/phase_pair_backlash_candidate.json:17` SHA256 `4e597d88f4b188e608a26c6591b5d8177e8f95af4973459baa3d67233931ce4f`
- 근거: `analysis/final_validation/results/v0.8/loaded_phase.json:561` SHA256 `8387e5a9f23ba1c7f58288b1a7bdb5af72fd10f529c033ea1fc8783171779dd5`

## TS-04 — PASS

CUT-03 front plate ↔ CUT-03 rear plate

- 원본 치수: seat-axis parallelism
- 계산: match-machine both plates and inspect the resulting pair
- 결과: 0 … 0.05 mm/140mm / 요구: parallelism ≤0.05/140 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:70` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/CUT-03/drawing_notes.md:8` SHA256 `474ab7438af4f1c656c03d16c1c0bddb7f8c4877009e0f36e4b32e1a7495368e`

## TS-05 — PASS

EX-SCR-01 flight ↔ EX-BAR-01 bore

- 원본 치수: radial cold clearance
- 계산: (ID limit − OD opposite limit) / 2
- 결과: 0.14 … 0.16 mm / 요구: 0.14 ≤ radial cold clearance ≤ 0.16 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:91` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`
- 근거: `exports/cnc/extruder/parts/EX-SCR-01/drawing_notes.md:7` SHA256 `d55e22134441cbeea2b6fb2cc6b32932d20378984c157e8e9a72fb881699eab4`

## TS-06 — PASS

EX-BAR-01 bore axis ↔ EX-DIE-01 channel axis

- 원본 치수: axis offset
- 계산: 0.010 barrel axis error +0.010 die axis error +0.004 maximum radial dowel play =0.024 mm
- 결과: 0 … 0.024 mm / 요구: axis offset ≤0.05 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:112` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`
- 근거: `exports/cnc/extruder/parts/EX-DIE-01/drawing_notes.md:7` SHA256 `d63cce8454f006b64cf9862f9d214097a48acea87a2ed11edfe9f31d85c04e74`

## TS-07 — PASS

TH-BH-01 heater free-state ID ↔ EX-BAR-01 OD

- 원본 치수: usable split-closure reserve
- 계산: minimum closure reserve=1.00−π(34.20−33.97)=0.277434 mm
- 결과: 0.277434 … None mm / 요구: usable closure reserve≥0.25 mm; physical 8-sector contact inspection remains NOT_RUN / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:133` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/thermal/parts/TH-BH-01/drawing_notes.md:7` SHA256 `0d44b5cf15c774f5e08f734e002ad67d657dfdfc248e1a170cb192f2d3efe246`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`

## TS-08 — PASS

TEMP-01..03 bore tip ↔ EX-BAR-01 melt bore

- 원본 치수: remaining ligament
- 계산: 16.985−8.110−5.450−0.050−1.625*sin(atan(0.10/5.5)); conservative flat-tip screen
- 결과: 3.345459 … None mm / 요구: released minimum ligament≥3.32 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:154` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`
- 근거: `cad/generation/generate_manufacturing.py:657` SHA256 `48429f72b2b883acccb45bcba53605b4f1c15d0778863f17df84b0b3cb971719`

## TS-09 — PASS

FD-MET-02 auger ↔ FD-MET-01 housing

- 원본 치수: radial running clearance
- 계산: (housing ID limit − auger OD opposite limit) / 2
- 결과: 0.2 … 0.25 mm / 요구: 0.2 ≤ radial running clearance ≤ 0.25 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:175` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/fabrication/parts/FD-MET-01/drawing_notes.md:7` SHA256 `669436a19a020d672ac6e7a087297201bba82de82a1511fd02cd9c5c12a20361`
- 근거: `exports/fabrication/parts/FD-MET-02/drawing_notes.md:7` SHA256 `fc3cf0c896820ce728b1421eab4f6296a466bce31f8f26ad24cb8d5d94e6e830`

## TS-10 — PASS

FM-RL-01 roller pair ↔ FM-EB-01 eccentric pair

- 원본 치수: 1.80 nominal unloaded gap
- 계산: adjust paired eccentric bushes equally, then measure the complete rotation
- 결과: 1.6 … 1.9 mm / 요구: 1.6 ≤ 1.80 nominal unloaded gap ≤ 1.9 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:196` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/fabrication/parts/FM-RL-01/drawing_notes.md:7` SHA256 `a9ee1a3297f4d48719c223958e83d77b34ab2dfc7b106f3420c918fc66abd64e`
- 근거: `exports/fabrication/parts/FM-PL-01/drawing_notes.md:7` SHA256 `bc36dfcacf5739e6b9fc937e357a87c77778bf04080f58511f90828d22960ef8`
- 근거: `exports/fabrication/parts/FM-EB-01/drawing_notes.md:7` SHA256 `20641707981d536ba70812ba6347942f2037b8138403304aae7b46854cbd28ef`

## TS-11 — PASS

PPR-C06 X gauge ↔ PPR-C06 Y gauge

- 원본 치수: optical centreline offset
- 계산: align both optical centres to one calibration wire, match-drill, fasten, then directly accept measured X/Y offset
- 결과: 0 … 0.1 mm / 요구: offset ≤0.10 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:217` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `cad/freecad/compact/geometry.py:813` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`

## TS-12 — PASS

SP-TR-01 matched end-plate pair ↔ installed Ø8 rods

- 원본 치수: assembled rod parallelism
- 계산: match-machine the end plates, install the selected rods, then inspect the complete 160 mm span
- 결과: 0 … 0.1 mm/160mm / 요구: 0 ≤ assembled rod parallelism ≤ 0.1 mm/160mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:238` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/fabrication/parts/SP-TR-01/drawing_notes.md:7` SHA256 `a1d1591a7d9b2fe656ef1e12d53c919a415518a2f02fc32cc9c0aa09daac87ff`

## TS-13 — PASS

guards/panels ↔ moving envelopes

- 원본 치수: 3.500 minimum released B-Rep clearance
- 계산: 3.500 ± (0.5 + 0.5) = 2.500–4.500
- 결과: 2.5 … 4.5 mm / 요구: moving clearance ≥2.0 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:259` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/fabrication/parts/DRV-GD-01/drawing_notes.md:7` SHA256 `32740dbfbe19acb05700a0fa839c10bf4e21d2449e984073688b042e40c9d7fd`
- 근거: `cad/freecad/compact/geometry.py:814` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `validation/results/full_motion.json:32` SHA256 `7f7a3b69c8f5658344e69a2ce4a6e8fb7fc58aaaedf3961dbe36635daf918d71`

## TS-14 — PASS

hot shield ↔ 300 °C hot envelope

- 원본 치수: 12.0 static clearance
- 계산: 12.000 ± (1.0 + 1.0) = 10.000–14.000
- 결과: 10.0 … 14.0 mm / 요구: hot clearance ≥10.0 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:280` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/fabrication/parts/EX-SH-01/drawing_notes.md:7` SHA256 `7fea58ffa9d2858c1a3f9137f9f3103bd3487299c215b3f20bf74ba0cb15786f`
- 근거: `cad/freecad/compact/geometry.py:812` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `validation/results/full_motion.json:28` SHA256 `7f7a3b69c8f5658344e69a2ce4a6e8fb7fc58aaaedf3961dbe36635daf918d71`

## TS-15 — PASS

ExtruderFrontSlidingGuide ↔ EX-BAR-01

- 원본 치수: remaining axial thermal margin
- 계산: current hot-zone qualification: declared cold travel minus worst 300 C full-length free growth
- 결과: 0.1672 … None mm / 요구: remaining travel ≥0 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:301` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/final/manufacturing/RFQ/manifest.csv:59` SHA256 `9360a4c78f7053bc36e341eca7a30a4403ffd6ebeb8b6587e84703ffaafdcec2`
- 근거: `analysis/final_validation/results/v0.8/hot_zone_digital_qualification.json:23` SHA256 `f1106f7fe2eeeca1ac041627cc6cd603aeab71cfec8ea5cb56b2e606ebefc4d9`

## TS-16 — PASS

EX-SCR-01 flight ↔ EX-BAR-01 bore

- 원본 치수: radial hot differential clearance
- 계산: minimum radial clearance over all current hot-zone differential-expansion sensitivity cases
- 결과: 0.137152 … 0.143978 mm / 요구: hot radial clearance ≥0.13 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:calculations/tolerance_stack_final.json:322` SHA256 `df709b616c41945f08e308dd404d4d3690bbb7a7f159bc1b72bb722b6696c4e5`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`
- 근거: `exports/cnc/extruder/parts/EX-SCR-01/drawing_notes.md:7` SHA256 `d55e22134441cbeea2b6fb2cc6b32932d20378984c157e8e9a72fb881699eab4`
- 근거: `analysis/final_validation/results/v0.8/hot_zone_digital_qualification.json:65` SHA256 `f1106f7fe2eeeca1ac041627cc6cd603aeab71cfec8ea5cb56b2e606ebefc4d9`

## IF-001 — PASS

CUT-05/CUT-05R ↔ SKF 61905-2RS1

- 원본 치수: shaft24.987-25.000 / bearing bore24.990-25.000
- 계산: bearing bore opposite limit - shaft opposite limit = -0.010–+0.013 mm
- 결과: -0.01 … 0.013 mm / 요구: diametral transition fit -0.010–+0.013 mm; receipt gauge and press/rotation check required / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:2` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/CUT-05/drawing_notes.md:8` SHA256 `b8c1d480c8c503a81afc964e7ffc29643a6e3c1bfd2e5a5d3b7fa23c2eadb0fe`
- 근거: `docs/final/61905_interface_basis_ko.md:8` SHA256 `2b1425a4916ec84d3002ff901a4504a277366268872447fe20f46f2a400cd997`

## IF-002 — PASS

SKF 61905-2RS1 ↔ CUT-03

- 원본 치수: bearing OD41.989-42.000 / seat42.000-42.025 H7
- 계산: housing seat opposite limit - bearing OD opposite limit = 0.000–0.036 mm
- 결과: 0 … 0.036 mm / 요구: stationary outer-ring H7 fit 0.000–0.036 mm; retainer and receipt inspection required / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:3` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/CUT-03/drawing_notes.md:8` SHA256 `474ab7438af4f1c656c03d16c1c0bddb7f8c4877009e0f36e4b32e1a7495368e`
- 근거: `docs/final/61905_interface_basis_ko.md:9` SHA256 `2b1425a4916ec84d3002ff901a4504a277366268872447fe20f46f2a400cd997`

## IF-003 — PASS

SKF 61905-2RS1 ↔ CUT-03/CUT-10

- 원본 치수: 0.125 axial float
- 계산: shim rear outer-ring retention, then accept each shaft directly by dial indicator over one full hand rotation
- 결과: 0.05 … 0.2 mm / 요구: 0.05 ≤ 0.125 axial float ≤ 0.2 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:4` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/CUT-03/drawing_notes.md:8` SHA256 `474ab7438af4f1c656c03d16c1c0bddb7f8c4877009e0f36e4b32e1a7495368e`
- 근거: `exports/cnc/CUT-10/drawing_notes.md:8` SHA256 `4d1c044f7093b17f4e91359fb34f94db9776ed722b09bd211118292620b2c18a`
- 근거: `docs/final/61905_interface_basis_ko.md:10` SHA256 `2b1425a4916ec84d3002ff901a4504a277366268872447fe20f46f2a400cd997`

## IF-004 — PASS

CUT-05/CUT-05R ↔ CUT-01/CUT-02

- 원본 치수: shaft24.987-25.000; cutter bore25.010-25.020; spacer bore25.100-25.150
- 계산: CUT-01 diametral clearance0.010–0.033; CUT-02 clearance0.100–0.163 mm
- 결과: 0.01 … 0.163 mm / 요구: cutter clearance0.010–0.033 and non-torque spacer clearance0.100–0.170 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:5` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/CUT-05/drawing_notes.md:8` SHA256 `b8c1d480c8c503a81afc964e7ffc29643a6e3c1bfd2e5a5d3b7fa23c2eadb0fe`
- 근거: `exports/cnc/CUT-01/drawing_notes.md:8` SHA256 `951f419b6c5e4a0eec79ba69bbac37449e4aa406204c1b6dd7789b5a609ac629`
- 근거: `exports/cnc/CUT-02/drawing_notes.md:8` SHA256 `fc8793eda97780e80c31fec2e48331ec7c6f6fbfc7e07d98772c554488ebf5f4`

## IF-005 — PASS

CUT-05R ↔ DRV-02

- 원본 치수: shaft24.987-25.000 / hub25.010-25.030; key5.995-6.000 / ways6.005-6.010
- 계산: hub bore - shaft =0.010–0.043; key side clearance=0.005–0.015 mm
- 결과: 0.01 … 0.043 mm / 요구: diametral clearance0–0.050 and key side clearance0.005–0.015 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:6` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/CUT-05R/drawing_notes.md:8` SHA256 `073554abc43881991e5d3f3d36cbbb714d8abdf1a9d50896e05a41af0207b73e`
- 근거: `exports/drive_interface/parts/DRV-02/drawing_notes.md:7` SHA256 `c638590a73e76d47a8b4077d63b5c99f08e87348cf53b9c5d7cdb575889d66e9`

## IF-006 — PASS

DRV-02 ↔ #35 30T sprocket blank

- 원본 치수: match-drilled 4×Ø6.6 PCD36.00±0.05; face≥6; assembled tooth-root TIR≤0.10
- 계산: hub used as drill jig; assembled tooth-root radial TIR measured over one full revolution =0.000–0.100 mm
- 결과: 0 … 0.1 mm / 요구: face≥6 mm; 4×Ø6.6 PCD36.00±0.05; assembled tooth-root radial TIR0–0.10 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:7` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/drive_interface/parts/DRV-02/drawing_notes.md:7` SHA256 `c638590a73e76d47a8b4077d63b5c99f08e87348cf53b9c5d7cdb575889d66e9`

## IF-007 — PASS

#35 chain ↔ 12T/30T sprockets + DRV-A60

- 원본 치수: pitch9.525; 40 pitches; calculated C86.167 within slot range81–99; slack2–3%
- 계산: ANSI two-sprocket equation for p9.525, z12/30, L40 gives C=86.167 mm; 18 mm chain-direction slots about nominal90 give81–99 mm
- 결과: 86.167 … 86.167 mm / 요구: calculated C86.0–86.3 lies within slot range; final pitch-plane offset≤0.20/150, slack2–3%, no tight spot in20 hand turns / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:8` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/drive_interface/parts/DRV-01/drawing_notes.md:7` SHA256 `07b3cdac504fa6ba3daf177a270e1f603233b64844508977ca5729b20bffa6f2`
- 근거: `exports/drive_interface/parts/DRV-A60/drawing_notes.md:7` SHA256 `99bd4bc371f04ffd68a8679162a8a6992c2804b92f5afcdd5904f6f152201ef4`

## IF-008 — PASS

TT Motor GMP60-60127-2460 ratio47 reference ↔ DRV-A60/DRV-F01A

- 원본 치수: pilot31.95–32.00/bore32.05–32.10; shaft11.95–12.00/D-bore12.02–12.05; flat10.85–10.90/10.92–10.95
- 계산: pilot diametral clearance0.05–0.15; shaft circle and D-flat clearance0.02–0.10; reported interval spans all controlled gaps
- 결과: 0.02 … 0.15 mm / 요구: pilot diametral clearance0.05–0.15; shaft circle and flat clearance0.02–0.10; M5 hole/PCD within stated receipt limits; D-flat bearing SF≥2 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:9` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/drive_interface/parts/DRV-A60/drawing_notes.md:7` SHA256 `99bd4bc371f04ffd68a8679162a8a6992c2804b92f5afcdd5904f6f152201ef4`
- 근거: `exports/drive_interface/parts/DRV-F01A/drawing_notes.md:7` SHA256 `ae9507e9d6e20c3200d542340423dca49dc9ef56007afa26a9f6e44231f58ae3`
- 근거: `docs/final/gmp60_reference_interface_basis_ko.md:49` SHA256 `326f4fab855a3978e11ef35f6dbb78a0566910474319d6e69e8d3d1b434e41e8`

## IF-009 — PASS

DRV-03/DRV-03R ↔ CUT-05/CUT-05R + selected key

- 원본 치수: bore25.010-25.020 / shaft24.987-25.000; key7.995-8.000 / ways8.005-8.010
- 계산: gear bore - shaft =0.010–0.033; key side clearance=0.005–0.015 mm
- 결과: 0.01 … 0.033 mm / 요구: diametral clearance0–0.040 and key side clearance0.005–0.015 mm; TS-03 controls loaded phase / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:10` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/drive_interface/parts/DRV-03/drawing_notes.md:7` SHA256 `29707f6e163aaa9bb2e1098af15feae1358b095d79e249b68d132c80bc1f1002`
- 근거: `exports/drive_interface/parts/DRV-03R/drawing_notes.md:7` SHA256 `eac6107619dd6f11a6c476590e0c580100b39cc264174d76e78bbbd057a5d0d0`
- 근거: `exports/cnc/CUT-05/drawing_notes.md:8` SHA256 `b8c1d480c8c503a81afc964e7ffc29643a6e3c1bfd2e5a5d3b7fa23c2eadb0fe`
- 근거: `exports/cnc/CUT-05R/drawing_notes.md:8` SHA256 `073554abc43881991e5d3f3d36cbbb714d8abdf1a9d50896e05a41af0207b73e`

## IF-010 — PASS

FM-GA-01 ↔ SKF 625-2Z

- 원본 치수: shaft4.992-5.000 / bearing bore4.992-5.000
- 계산: 625 bore opposite limit - FM-GA-01 shaft opposite limit = -0.008–+0.008 mm
- 결과: -0.008 … 0.008 mm / 요구: diametral transition fit -0.008–+0.008 mm; receipt gauge and free-rotation check required / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:11` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FM-GA-01/drawing_notes.md:7` SHA256 `1407b8b6009de02e16bb37373d108a9dcc55e7d185dc0f3d8733aaeda29185e1`
- 근거: `docs/final/625_6001_interface_basis_ko.md:8` SHA256 `1971287a63798164a55347badec00e2076558aebdd633b726e497454da0413c0`

## IF-011 — PASS

SKF 625-2Z ↔ FM-GR-01/FM-GC-01

- 원본 치수: bearingOD15.992-16.000 / seat16.000-16.018 H7; pocket5.10 / width4.880-5.000; cap bore15.00-15.10
- 계산: 23°C clearance=0.000–0.026; at60°C add (130−12)e-6×16×37=0.0699; bound=0.000–0.096 mm; pocket−width=0.100–0.220; cap overlap=0.446–0.500
- 결과: 0 … 0.096 mm / 요구: 23–60°C diametral clearance0–0.100; axial clearance0.10–0.22; outer-ring overlap≥0.44; assembled roller TIR≤0.10 and no outer-ring creep / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:12` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FM-GR-01/drawing_notes.md:7` SHA256 `fccf37d860afae67000cf3ef54eddc62623d3abefe3b4cee91cc2f1edfb2d78f`
- 근거: `exports/fabrication/parts/FM-GC-01/drawing_notes.md:7` SHA256 `9c86f9cc3e8dfc3e9cedb2cbb4d582cebff80e49ce12de9907a1addb7fec03c7`
- 근거: `docs/final/625_6001_interface_basis_ko.md:8` SHA256 `1971287a63798164a55347badec00e2076558aebdd633b726e497454da0413c0`

## IF-012 — PASS

FM-GA-01 ↔ PPR-C08 ×2

- 원본 치수: shaft4.992-5.000 / finished bores5.20-5.40; loose T-slot alignment
- 계산: finished bore opposite limit - h6 axle opposite limit =0.200–0.408 mm
- 결과: 0.2 … 0.408 mm / 요구: 0.180–0.450 mm diametral clearance; one axle passes both aligned brackets by hand without visible bending / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:13` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FM-GA-01/drawing_notes.md:7` SHA256 `1407b8b6009de02e16bb37373d108a9dcc55e7d185dc0f3d8733aaeda29185e1`
- 근거: `cad/freecad/compact/geometry.py:815` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`

## IF-013 — PASS

FM-RL-01 roller pair ↔ FM-EB-01/FM-PL-01

- 원본 치수: 1.80 nominal unloaded gap
- 계산: adjust paired eccentric bushes equally, then measure the complete rotation
- 결과: 1.6 … 1.9 mm / 요구: 1.6 ≤ 1.80 nominal unloaded gap ≤ 1.9 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:14` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FM-RL-01/drawing_notes.md:7` SHA256 `a9ee1a3297f4d48719c223958e83d77b34ab2dfc7b106f3420c918fc66abd64e`
- 근거: `exports/fabrication/parts/FM-EB-01/drawing_notes.md:7` SHA256 `20641707981d536ba70812ba6347942f2037b8138403304aae7b46854cbd28ef`
- 근거: `exports/fabrication/parts/FM-PL-01/drawing_notes.md:7` SHA256 `bc36dfcacf5739e6b9fc937e357a87c77778bf04080f58511f90828d22960ef8`

## IF-014 — PASS

SP-AX-01 ↔ SP-DA-01/SP-RL-01/SP-DS-01

- 원본 치수: shaft7.991-8.000 / bores8.200-8.250; motion±25deg
- 계산: reamed bore opposite limit - h6 axle opposite limit =0.200–0.259 mm
- 결과: 0.2 … 0.259 mm / 요구: diametral running clearance0.180–0.300 mm and free motion under0.2–1.0 N filament tension / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:15` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/SP-AX-01/drawing_notes.md:7` SHA256 `a323480cdffe9ffe8e4a0d5624fbfd042b04b4865cac77d33b40a77c142b0c69`
- 근거: `exports/fabrication/parts/SP-DA-01/drawing_notes.md:7` SHA256 `e81f49642572e88489d5955035c2ce4b2fbab888ee77c24001c4a0e28a35485a`
- 근거: `exports/fabrication/parts/SP-RL-01/drawing_notes.md:7` SHA256 `2c5dd5cf37030274f49f296693edd02621ea70d2a15aee8e4d452f2d0cdc8fce`
- 근거: `exports/fabrication/parts/SP-DS-01/drawing_notes.md:7` SHA256 `8456524f47d1d1b4159d7ab3f7ca379f06f764e505c3952735c20dc9fef2e8cd`

## IF-015 — PASS

2× Ø8 h6 ground steel rods ↔ PPR-C10/SP-TR-01

- 원본 치수: rods7.991-8.000 / carriage8.40-8.50 / end plates8.20-8.30
- 계산: end-plate clearance0.200–0.309; carriage clearance0.400–0.509 mm
- 결과: 0.2 … 0.509 mm / 요구: end-plate diametral clearance0.180–0.350; carriage0.350–0.550; TS-12 controls pair parallelism / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:16` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `cad/freecad/compact/geometry.py:817` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `exports/fabrication/parts/SP-TR-01/drawing_notes.md:7` SHA256 `a1d1591a7d9b2fe656ef1e12d53c919a415518a2f02fc32cc9c0aa09daac87ff`

## IF-016 — PASS

SP-SH-01 ↔ SKF 6001-2RSH

- 원본 치수: shaft11.989-12.000 / bearing bore11.992-12.000
- 계산: 6001 bore opposite limit - SP-SH-01 shaft opposite limit = -0.008–+0.011 mm
- 결과: -0.008 … 0.011 mm / 요구: diametral transition fit -0.008–+0.011 mm; receipt gauge and free-rotation check required / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:17` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/SP-SH-01/drawing_notes.md:7` SHA256 `357622abbeebf22825350ce4784661fc331a5bf79568206db6453740fed891db`
- 근거: `docs/final/625_6001_interface_basis_ko.md:9` SHA256 `1971287a63798164a55347badec00e2076558aebdd633b726e497454da0413c0`

## IF-017 — PASS

SKF 6001-2RSH ↔ SP-BP-01/SP-BR-01

- 원본 치수: bearingOD27.991-28.000 / seat28.000-28.021 H7; pocket8.05-8.10 / bearing width7.880-8.000; retainer relief26.00-26.10
- 계산: seat−OD=0.000–0.030 mm; pocket−width=0.050–0.220 mm axial clearance; retainer radial overlap=0.9455–1.000 mm
- 결과: 0 … 0.03 mm / 요구: diametral clearance0–0.036; axial clearance0.05–0.22; outer-ring overlap≥0.90 mm; no seal/inner-ring contact / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:18` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/SP-BP-01/drawing_notes.md:7` SHA256 `f7b00959399ebde26c4afef7e7dbb356b6d495670aee2aeda49032f9ea414a54`
- 근거: `exports/fabrication/parts/SP-BR-01/drawing_notes.md:7` SHA256 `e149782be376687dac7c4946da549a4f53a4d89d208b7d5fea04fc243ade2582`
- 근거: `docs/final/625_6001_interface_basis_ko.md:9` SHA256 `1971287a63798164a55347badec00e2076558aebdd633b726e497454da0413c0`

## IF-018 — PASS

PPR-C09 ↔ SP-SH-01/received spool

- 원본 치수: finished bore12.20-12.40 / shaft11.989-12.000; M6 through clamp
- 계산: finished adapter bore opposite limit - h6 spindle opposite limit =0.200–0.411 mm
- 결과: 0.2 … 0.411 mm / 요구: 0.180–0.450 mm diametral clearance; M6 clamp prevents slip and metal collar carries axial load / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:19` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `cad/freecad/compact/geometry.py:816` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `exports/fabrication/parts/SP-SH-01/drawing_notes.md:7` SHA256 `357622abbeebf22825350ce4784661fc331a5bf79568206db6453740fed891db`

## IF-019 — PASS

EX-SCR-01 ↔ EX-BAR-01

- 원본 치수: radial cold clearance
- 계산: (ID limit − OD opposite limit) / 2
- 결과: 0.14 … 0.16 mm / 요구: 0.14 ≤ radial cold clearance ≤ 0.16 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:20` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/extruder/parts/EX-SCR-01/drawing_notes.md:7` SHA256 `d55e22134441cbeea2b6fb2cc6b32932d20378984c157e8e9a72fb881699eab4`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`

## IF-020 — PASS

EX-SCR-01 thrust seat/shoulder ↔ NSK 51102/EX-THR-01

- 원본 치수: seat14.982-15.000 / shoulder23.00-23.05; bearing15×28×9; pocket28.30-28.35×9.10-9.15
- 계산: plate pocket - bearing OD =0.300–0.350 mm diametral; shaft abutment minimum23.00 mm; housing abutment17.20 mm
- 결과: 0.3 … 0.35 mm / 요구: housing diametral clearance>0.25 mm; shaft abutment≥23 mm; housing abutment≤20 mm; shim-set loaded-direction endplay0.05–0.15 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:21` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/extruder/parts/EX-SCR-01/drawing_notes.md:7` SHA256 `d55e22134441cbeea2b6fb2cc6b32932d20378984c157e8e9a72fb881699eab4`
- 근거: `exports/fabrication/parts/EX-THR-01/drawing_notes.md:7` SHA256 `ae99460a763f9dee748805405d1d58f4d8d3c0e0d1e138c09a4f2aaa17fccfe9`
- 근거: `analysis/final_validation/results/v0.8/extruder_thrust_stack_candidate.json:75` SHA256 `e4e77eeeda3310a03af407927cd53b4288ffad7b2cb3db91ed22e9942db18746`

## IF-021 — PASS

FD-MET-02 ↔ FD-MET-01

- 원본 치수: radial running clearance
- 계산: (housing ID limit − auger OD opposite limit) / 2
- 결과: 0.2 … 0.25 mm / 요구: 0.2 ≤ radial running clearance ≤ 0.25 mm / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:22` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FD-MET-02/drawing_notes.md:7` SHA256 `fc3cf0c896820ce728b1421eab4f6296a466bce31f8f26ad24cb8d5d94e6e830`
- 근거: `exports/fabrication/parts/FD-MET-01/drawing_notes.md:7` SHA256 `669436a19a020d672ac6e7a087297201bba82de82a1511fd02cd9c5c12a20361`

## IF-022 — PASS

FD-MET-03 ↔ FD-MET-02/FD-CP-01/EG17-G10

- 원본 치수: shaft7.978-8.000; auger bore8.200-8.300; coupling bores8.050-8.080; matched Ø3.00-3.05 cross-holes
- 계산: FD-CP-01 bore opposite limit − shaft opposite limit =0.050–0.102; auger clearance0.200–0.322; gearbox rating SF=5/2.2=2.273; both spring-pin static screens SF≥2
- 결과: 0.05 … 0.102 mm / 요구: coupling diametral clearance0.03–0.12; auger clearance0.15–0.35; pin/boss and gearbox SF≥2 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:23` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FD-MET-03/drawing_notes.md:7` SHA256 `ed21867f0679901815e676fc12a9f54fbc7ffb4af4f21813220495bb42109117`
- 근거: `exports/fabrication/parts/FD-MET-02/drawing_notes.md:7` SHA256 `fc3cf0c896820ce728b1421eab4f6296a466bce31f8f26ad24cb8d5d94e6e830`
- 근거: `exports/fabrication/parts/FD-CP-01/drawing_notes.md:7` SHA256 `616474fb68261f62a36b326caf3eabc74355673b88f1e980b5c81a28a9454e9d`
- 근거: `exports/fabrication/parts/FD-DA-01/drawing_notes.md:7` SHA256 `eaf339ffee85dea3ee4d2713a089e3a684fd37b24258b8a8dcd2b987b971edea`
- 근거: `docs/final/feeder_reference_drive_ko.md:9` SHA256 `f33c76834a9c0e62f57845bf765092af9ab67122386c6bae4870d91c38a6b5d7`

## IF-023 — PASS

EX-BAR-01 ↔ TH-BH-01 ×3

- 원본 치수: usable split-closure reserve
- 계산: minimum closure reserve=1.00−π(34.20−33.97)=0.277434 mm
- 결과: 0.277434 … None mm / 요구: usable closure reserve≥0.25 mm; physical 8-sector contact inspection remains NOT_RUN / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:24` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`
- 근거: `exports/thermal/parts/TH-BH-01/drawing_notes.md:7` SHA256 `0d44b5cf15c774f5e08f734e002ad67d657dfdfc248e1a170cb192f2d3efe246`

## IF-024 — PASS

EX-DIE-01 ↔ TH-DIE-01

- 원본 치수: boreØ6.55 H7 =6.550–6.565 / Tempco Type CG heater6.487–6.513
- 계산: opposite limits: [6.550−6.513,6.565−6.487]=0.037–0.078 mm diametral; radial0.0185–0.0390 mm
- 결과: 0.037 … 0.078 mm / 요구: diametral clearance0.030–0.090; radial clearance≤0.05; metal flange positively retains heater / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:25` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/extruder/parts/EX-DIE-01/drawing_notes.md:7` SHA256 `d63cce8454f006b64cf9862f9d214097a48acea87a2ed11edfe9f31d85c04e74`
- 근거: `exports/thermal/parts/TH-DIE-01/drawing_notes.md:7` SHA256 `ff5cd1a16831b240d418fee6206aba3a1350fa1501583bb7fe5fb0754fe33895`
- 근거: `calculations/run_engineering.py:221` SHA256 `9b011de99355acf3fab2c06fd390338eae7c84b4c6595183c7a2a019664c78b6`
- 근거: `docs/final/die_heater_selection_basis_ko.md:17` SHA256 `cd0fec430db37dd96f6bfc3fa508f3263e18028c97854868b2a8e75b3dc14854`

## IF-025 — PASS

EX-BAR-01 ↔ TH-TC-01 at TEMP-01..03

- 원본 치수: bore3.20-3.25 flat-bottom depth5.35-5.45 / probe2.97-3.03 / stop5.15-5.25
- 계산: bore minus probe opposite limits=3.20-3.03 to3.25-2.97=0.17-0.28; bottom gap=5.35-5.25 to5.45-5.15=0.10-0.30 mm
- 결과: 0.17 … 0.28 mm / 요구: diametral clearance0.15-0.30; tip gap0.10-0.30; positive metal stop retention; receipt bias<=2 C and t90<=30 s / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:26` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/extruder/parts/EX-BAR-01/drawing_notes.md:7` SHA256 `4814d0fbf1d00eab886da724fe66ccc613536eaf909013384aefe41d0c0bffa5`
- 근거: `exports/thermal/parts/TH-TC-01/drawing_notes.md:7` SHA256 `872b98c0f67da81da24002980ae55c1d9a6e3da5daf378185fde4d6c42a677e8`
- 근거: `docs/final/thermocouple_selection_basis_ko.md:11` SHA256 `0d07e90e49bbd08c06a8129eb2a0d9d306a4c24af348fc78eee35a3c4ae1d44b`

## IF-026 — PASS

EX-DIE-01 ↔ TH-TC-01 at TEMP-04

- 원본 치수: bore3.20-3.25 depth11.95-12.05 / probe2.97-3.03 / stop9.95-10.05
- 계산: bore minus probe=0.17-0.28; bottom gap=11.95-10.05 to12.05-9.95=1.90-2.10; nearest heater-channel surface gap>=7.47 mm
- 결과: 0.17 … 0.28 mm / 요구: diametral clearance0.15-0.30; bottom gap1.90-2.10; channel ligament>=6.0; positive metal stop retention / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:27` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/cnc/extruder/parts/EX-DIE-01/drawing_notes.md:7` SHA256 `d63cce8454f006b64cf9862f9d214097a48acea87a2ed11edfe9f31d85c04e74`
- 근거: `exports/thermal/parts/TH-TC-01/drawing_notes.md:7` SHA256 `872b98c0f67da81da24002980ae55c1d9a6e3da5daf378185fde4d6c42a677e8`
- 근거: `docs/final/thermocouple_selection_basis_ko.md:15` SHA256 `0d07e90e49bbd08c06a8129eb2a0d9d306a4c24af348fc78eee35a3c4ae1d44b`

## IF-027 — PASS

removed hopper-maintenance PTC ↔ external predry architecture

- 원본 치수: no active mating interface
- 계산: hopper-maintenance PTC, spreader, clamp, power output and purchase line removed; external predry remains
- 결과: 0 … 0 interfaces / 요구: zero active hopper-maintenance PTC interfaces / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:28` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `docs/final/release_notes_v1.0.0-rc1_ko.md:40` SHA256 `659ba1a67689684660ce918894f1ffb9ab114ea07bce26ef04c9924db60e9337`

## IF-028 — PASS

M3 through-bolts ↔ PPR-C06/PPR-C11

- 원본 치수: M3 major diameter≤3.00 / finished holes3.40-3.50
- 계산: finished hole3.40–3.50 minus M3 maximum major diameter3.00 = diametral clearance0.40–0.50 mm
- 결과: 0.4 … 0.5 mm / 요구: diametral clearance0.30–0.60; nuts and washers accessible from open enclosure/control-panel side; no heat-set inserts / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:29` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `cad/freecad/compact/geometry.py:813` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `cad/freecad/compact/geometry.py:818` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`

## IF-029 — PASS

M4 screw/washer/nyloc ↔ PPR-C01/PPR-C10

- 원본 치수: M4 major diameter≤4.00 / finished through bores4.50–4.70
- 계산: finished hole4.50–4.70 minus M4 maximum major diameter4.00 = diametral clearance0.50–0.70
- 결과: 0.5 … 0.7 mm / 요구: diametral clearance0.40–0.80; PPR-C01 flat-head flush/recessed≤0.05; no heat-set insert route / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:30` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `cad/freecad/compact/geometry.py:808` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `cad/freecad/compact/geometry.py:817` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`

## IF-030 — PASS

M3/M4/M5/M6 fasteners and spring pin ↔ individual printed/metal joints

- 원본 치수: 30 uniquely identified joint contracts
- 계산: 30 unique schedule joint IDs = 30 joint IDs referenced by generated assembly steps; every contract field nonblank
- 결과: 30 … 30 joints / 요구: all 30 unique joint contracts have parts/specification/quantity/torque/locking/tool/inspection/source/state and appear in assembly steps / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:31` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `cad/freecad/compact/geometry.py:809` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `cad/freecad/compact/geometry.py:810` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `cad/freecad/compact/geometry.py:811` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `exports/cnc/CUT-03/drawing_notes.md:8` SHA256 `474ab7438af4f1c656c03d16c1c0bddb7f8c4877009e0f36e4b32e1a7495368e`
- 근거: `exports/final/bom/fastener_schedule.csv:1` SHA256 `2f56d5f75cd8f4202f5e81bbc167de95391ef563176dbce8d3b1f9596742c254`
- 근거: `docs/final/assembly_steps.csv:1` SHA256 `311870833778f1a97da27be26e86501063eb9f0ede48f1e44334602216853771`

## IF-031 — PASS

FD-HOP-01/FD-GSK-01 ↔ FD-MET-01 registered flange

- 원본 치수: spigot28.77–28.80 / socket28.90–28.93; hopper flow24.90–25.00 / housing25.00–25.05; gasket compressed0.35–0.40
- 계산: socket−spigot diametral clearance=0.10–0.16; downstream housing ID−upstream hopper ID=0.00–0.15; gasket ID clearance to largest flow bore≥0.15 mm
- 결과: 0.1 … 0.16 mm / 요구: register clearance0.08–0.18; nonnegative0–0.15 flow expansion; gasket must not intrude; compressed thickness0.35–0.40 / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:32` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `exports/fabrication/parts/FD-HOP-01/drawing_notes.md:7` SHA256 `99c859c8f3812b2ba5fa16dfc14565ff52b3725af000450a8f6fb2fa15ece2f9`
- 근거: `exports/fabrication/parts/FD-GSK-01/drawing_notes.md:7` SHA256 `d735eea35c54713b05bb2a446760a9868d1dd7f549a8def9d3d9f9f2aa0d7cd0`
- 근거: `exports/fabrication/parts/FD-MET-01/drawing_notes.md:7` SHA256 `669436a19a020d672ac6e7a087297201bba82de82a1511fd02cd9c5c12a20361`

## IF-032 — PASS

PPR-C03 ×4 ↔ FD-BIN-01

- 원본 치수: sheet1.00±0.05; printed slot1.40±0.30
- 계산: slot opposite limit − sheet opposite limit = 0.05–0.75 mm
- 결과: 0.05 … 0.75 mm / 요구: 0.05 ≤ total slot clearance ≤ 0.75 mm; no inward burr/dead pocket / numeric PASS
- 미해결: 없음 — 명시된 디지털 범위 한정, 실물 미검증
- 근거: `f3b1e666c95e:exports/fabrication/interface_catalog.csv:33` SHA256 `2b553443b200a80ce3c87f0d11d3b2c737f26886a3339e6a1fe70be66267b6dc`
- 근거: `cad/freecad/compact/geometry.py:810` SHA256 `ca7867a5a50cb0fdb74387e8e8fe7b5b619102e2fed90c52fba5cb227de6fde7`
- 근거: `exports/fabrication/parts/FD-BIN-01/drawing_notes.md:7` SHA256 `042d664157d18dc087985564549e4de67896f01a19a9e29e3234556b7431a9c8`

Cutter/blade gap은 금속 shim만 사용한다. Cutter/screw/heater/high-current의 물리 검증은 물리 lockout과 사용자 확인 전 완료로 표시하지 않는다. 명시된 디지털 검증 범위의 완료는 물리·제작·운전 승인을 대체하지 않는다.
