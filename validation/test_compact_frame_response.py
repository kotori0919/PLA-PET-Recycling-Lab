"""Independent beam references and negative inputs for the placement review."""
import math
from pathlib import Path
import sys
import unittest
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.compact_layout_v08.frame_response import crossrail_response


class CompactFrameResponseTests(unittest.TestCase):
    def test_two_symmetric_point_loads(self):
        length, distance, total = 430.0, 100.0, 100.0
        result = crossrail_response([20+distance, 450-distance], [total/2,total/2], 86)
        expected = total*distance*(3*length**2-4*distance**2)/(48*69000*51400)
        self.assertAlmostEqual(result['max_deflection_mm'], expected, places=9)
        np.testing.assert_allclose(result['support_reactions_n'], [50,50], atol=1e-7)
        self.assertAlmostEqual(result['max_bending_moment_nmm'], 5000, places=8)

    def test_linearity(self):
        a = crossrail_response([72,202], [25,75])
        b = crossrail_response([72,202], [50,150])
        self.assertAlmostEqual(b['max_deflection_mm']/a['max_deflection_mm'], 2, places=9)
        self.assertAlmostEqual(b['work_nmm']/a['work_nmm'], 4, places=9)

    def test_actual_relocation_changes_reactions(self):
        old = crossrail_response([90,220], [50,50])
        new = crossrail_response([72,202], [50,50])
        self.assertGreater(new['support_reactions_n'][0], old['support_reactions_n'][0])
        self.assertLess(new['support_reactions_n'][1], old['support_reactions_n'][1])
        self.assertLess(new['reaction_error_n'], 1e-5)

    def test_unpowered_load_invalid(self):
        with self.assertRaises(ValueError):
            crossrail_response([72,202], [0,0])

    def test_invalid_positions(self):
        for points in ([19,202], [72,451], [202,72], [72,72], [math.nan,202], [72]):
            with self.subTest(points=points), self.assertRaises(ValueError):
                crossrail_response(points, [50,50])

    def test_invalid_forces(self):
        for forces in ([-1,100], [math.inf,50], [math.nan,50], [100]):
            with self.subTest(forces=forces), self.assertRaises(ValueError):
                crossrail_response([72,202], forces)

    def test_refinement(self):
        a = crossrail_response([72,202], [25,75], 32)
        b = crossrail_response([72,202], [25,75], 64)
        self.assertLess(abs(a['max_deflection_mm']/b['max_deflection_mm']-1), 0.01)


if __name__ == '__main__':
    unittest.main()
