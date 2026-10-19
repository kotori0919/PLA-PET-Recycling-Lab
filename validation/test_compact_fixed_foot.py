"""Compact layout preserves support datums and contains real aligned holes."""
import sys
import unittest
from pathlib import Path
import FreeCAD as App
import Part
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'cad/freecad/drive_v08')]
from cad.freecad.final_v08.generate import final_objects
from cad.freecad.drive_v08.assembly import integrated_objects
from analysis.compact_layout_v08.fixed_foot_layout import candidate, validate
from analysis.compact_layout_v08.review import by_name, dimensions, contact_area


class FixedFootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, _ = integrated_objects(final_objects(), compact_layout=False)
        cls.rows, cls.transforms, cls.holes = candidate(cls.base)
        cls.old, cls.new = by_name(cls.base), by_name(cls.rows)

    def test_same_inventory_and_envelope(self):
        self.assertEqual(set(self.old), set(self.new))
        for actual, expected in zip(dimensions(self.rows), (470, 700, 930)):
            self.assertAlmostEqual(actual, expected, places=6)

    def test_frame_and_four_feet_do_not_move(self):
        names = ['GGM_ShredRail', 'MidRail500']
        names += [n for n in self.old if n.startswith('GGM_SH_Spacer_')]
        self.assertEqual(len(names), 6)
        for name in names:
            with self.subTest(name=name):
                self.assertLess(self.old[name].cut(self.new[name]).Volume, 0.01)
                self.assertLess(self.new[name].cut(self.old[name]).Volume, 0.01)

    def test_existing_plate_stock_and_hole_count(self):
        a, b = self.old['GGM_SH_Base'], self.new['GGM_SH_Base']
        self.assertEqual(len(self.holes), 8)
        self.assertAlmostEqual(a.Volume, b.Volume, places=5)
        for axis in 'XYZ':
            self.assertAlmostEqual(getattr(a.BoundBox, axis+'Length'),
                                   getattr(b.BoundBox, axis+'Length'), places=6)
        self.assertTrue(b.isValid())
        self.assertEqual(len(b.Solids), 1)

    def test_all_eight_holes_and_mating_faces(self):
        plate = self.new['GGM_SH_Base']; pb = plate.BoundBox
        for hole in self.holes:
            name = hole['mating_object']; shape = self.new[name]
            with self.subTest(name=name):
                probe = Part.makeCylinder(hole['diameter_mm']/2-0.005, pb.ZLength,
                    App.Vector(hole['x_mm'], hole['y_mm'], pb.ZMin))
                self.assertLess(plate.common(probe).Volume, 0.01)
                self.assertGreater(contact_area(plate, shape), 1.0)
                self.assertAlmostEqual(shape.BoundBox.Center.x, hole['x_mm'], places=6)
                self.assertAlmostEqual(shape.BoundBox.Center.y, hole['y_mm'], places=6)

    def test_negative_added_component(self):
        bad = self.rows + [dict(self.rows[0], name='UNDECLARED_PART')]
        with self.assertRaisesRegex(ValueError, 'component addition or omission'):
            validate(self.base, bad, self.transforms, self.holes)

    def test_negative_floating_support(self):
        bad = [dict(r, shape=r['shape'].copy()) for r in self.rows]
        by_name(bad)['GGM_SH_Spacer_90_100'].translate(App.Vector(0, 0, 0.1))
        with self.assertRaisesRegex(ValueError, 'unrequested geometry change'):
            validate(self.base, bad, self.transforms, self.holes)

    def test_negative_moved_motor_only(self):
        bad = [dict(r, shape=r['shape'].copy()) for r in self.rows]
        by_name(bad)['GGM_Shredder'].translate(App.Vector(0, 1, 0))
        with self.assertRaisesRegex(ValueError, 'unrequested geometry change'):
            validate(self.base, bad, self.transforms, self.holes)


if __name__ == '__main__':
    unittest.main()
