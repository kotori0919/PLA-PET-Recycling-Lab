"""Keep frame interfaces while redrilling the same compact shelf plate."""
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'cad/freecad/drive_v08')]
from analysis.compact_layout_v08.fixed_foot_layout import candidate,validate
from analysis.compact_layout_v08.review import by_name
from cad.freecad.drive_v08.assembly import integrated_objects
from cad.freecad.final_v08.generate import final_objects

class FixedFootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base,_=integrated_objects(final_objects(), compact_layout=False)
        cls.rows,cls.transforms,cls.holes=candidate(cls.base)

    def copy(self): return [dict(r,shape=r['shape'].copy()) for r in self.rows]

    def test_unchanged_frame_and_feet(self):
        a,b=by_name(self.base),by_name(self.rows)
        for name in a:
            if name.startswith('GGM_SH_Spacer_') or name in ('MidRail500','GGM_ShredRail'):
                self.assertLess(a[name].cut(b[name]).Volume+b[name].cut(a[name]).Volume,0.01)
        self.assertEqual(len(self.holes),8)
        self.assertAlmostEqual(a['GGM_SH_Base'].Volume,b['GGM_SH_Base'].Volume,places=5)

