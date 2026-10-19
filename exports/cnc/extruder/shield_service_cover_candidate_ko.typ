#set page(paper: "a4", margin: 15mm)
#set text(font: "Noto Sans CJK KR", size: 9pt)
#let evidence = json("../../../analysis/final_validation/results/v0.8/retainer_tool_access.json")
#let covers = evidence.service_window_candidate
#let cover = covers.first()
#assert(covers.len() == 2)
#assert(cover.cover_box_mm.slice(3) == (28, 2, 68))
#assert(cover.hole_diameter_mm == 3.4)
#assert(cover.hole_centres_xz_mm.len() == 4)

= 점검 덮개 후보 — 가공 승인 금지 / HOLD
EX-SH-01 관련 미채택 부품 · 단위 mm · 정면도 2:1 · 수량 2

소재 후보: 기존 차열판과 같은 2 mm 5052 알루미늄 판.
재질 상태·치수 공차·체결품·표면처리·접지 본딩은 미확정이다.
본 도면은 가공 가능성 검토용이며 발주용이 아니다.

#align(center)[
  #box(width: 85mm, height: 145mm)[
    #place(top + left, dx: 10mm, dy: 5mm, rect(width: 56mm, height: 136mm, stroke: 0.6pt))
    #for point in cover.hole_centres_xz_mm {
      let x = point.at(0) - cover.cover_box_mm.at(0)
      let z = point.at(1) - cover.cover_box_mm.at(2)
      place(top + left, dx: (10 + 2*x - 3.4)*1mm,
        dy: (5 + 2*(68-z) - 3.4)*1mm,
        circle(radius: 3.4mm, stroke: 0.6pt))
    }
    #place(top + left, dx: 29mm, dy: 0mm)[28]
    #place(top + left, dx: 69mm, dy: 68mm)[68]
  ]
]

*기준:* 정면도 좌하단 = (0,0). 네 구멍은 Ø3.4 관통, 두께 2.
#table(columns: (1fr, 1fr, 1fr),
  [구멍], [X], [Z],
  ..cover.hole_centres_xz_mm.enumerate().map(((i, point)) => (
    str(i+1), str(point.at(0)-317), str(point.at(1)-348)
  )).flatten())

최소 명목 외곽 잔여 폭: #cover.cover_edge_ligament_mm mm. 강도 합격값이 아니다.
맞물리는 점검창은 12×52이며 덮개 중심과 일치한다(각 방향 겹침 8).
나사산 없음. 관통공만으로 체결·탈락 방지·PE 접지가 성립하지 않는다.
날카로운 모서리 제거 방법과 최종 치수 공차는 공급자 검토 후 확정한다.

*검증 범위:* STEP 단일 솔리드/부피와 명목 간섭만 검사했다.
체결 강도, 뜨거운 표면 접근 방지, 실제 공구·손 공간 및 물리 시험은 미검증이다.
