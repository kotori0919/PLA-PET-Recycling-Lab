import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.compact_layout_v08.shelf_strip_screen import beam_case


class ShelfStripTests(unittest.TestCase):
    def test_textbook_cantilever(self):
        row = beam_case((0,0), (50,0), 100)
        inertia = 20*6**3/12
        self.assertAlmostEqual(row['stress_mpa'], 6*100*50/(20*6**2), places=12)
        self.assertAlmostEqual(row['deflection_mm'], 100*50**3/(3*200000*inertia), places=12)

    def test_distance_increases_demand(self):
        short = beam_case((0,0),(20,0))
        long = beam_case((0,0),(60,0))
        self.assertGreater(long['stress_mpa'], short['stress_mpa'])
        self.assertGreater(long['deflection_mm'], short['deflection_mm'])
        self.assertLess(long['per_post_load_limit_n_at_sf2'], short['per_post_load_limit_n_at_sf2'])

    def test_actual_worst_geometry_is_bounded(self):
        row = beam_case((37,322),(90,280))
        self.assertGreater(row['yield_sf'], 2.0)
        self.assertLess(row['deflection_mm'], 0.5)
        self.assertTrue(math.isfinite(row['per_post_load_limit_n_at_sf2']))


if __name__ == '__main__':
    unittest.main()
