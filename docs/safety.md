# 안전 baseline

이 설계는 안전 인증 제품이 아니다. Cutter, screw, heater와 high-current branch는 물리 gate와 사용자 승인이 끝날 때까지 energize하지 않는다.

- Anti-reach path와 lid/service positive-opening interlock를 사용한다.
- E-stop/interlock/thermal fuse/branch fuse는 software와 독립된 cut path다.
- Cutter와 screw main load는 metal bearing/plate/profile로 전달한다.
- Hot path와 direct radiant path에 출력품을 두지 않는다. ABS duct도 metal shield 뒤의 cold side에 둔다.
- Die blockage는 open flow area, replaceable screen, calibrated torque trip와 guarded sacrificial retainer로 제한한다.
- Jam service는 main disconnect, 0 V, mechanical shaft block와 전용 tool 후 수행한다.
- First-hot-test는 shield 뒤 원격 stop, low feed, PLA부터 시행하고 PET는 dryness와 PLA gate 이후에만 시행한다.

실제 pressure, containment, PE bonding, insulation resistance, fuse coordination, heater runaway와 E-stop stopping time의 시험 기록 및 필요한 사용자 승인 없이는 물리 검증 완료·제작 승인·운전 승인으로 표시하지 않는다. 디지털 구현·계산·시뮬레이션은 명시한 범위에서 별도로 완료 판정할 수 있으나 현재 fabrication release 승인 요구를 대체하지 않는다.
