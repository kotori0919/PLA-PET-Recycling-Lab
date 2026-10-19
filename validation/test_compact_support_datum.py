"""Nominal solids and negative cases for the inset front-support correction."""
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'cad/freecad/drive_v08')]
from cad.freecad.final_v08.generate import final_objects
from cad.freecad.drive_v08.assembly import integrated_objects
from analysis.compact_layout_v08 import review as r
from analysis.compact_layout_v08.support_datum import proposal, check_mounts


class SupportDatumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base,_=integrated_objects(final_objects(), compact_layout=False)
        cls.candidate,cls.transforms=proposal(cls.base)

    def copy(self):
        return [dict(v,shape=v['shape'].copy()) for v in self.candidate]

    def test_contacts_and_shape_count(self):
        self.assertEqual(len(check_mounts(self.base,self.candidate)),12)
        self.assertEqual(len(self.base),len(self.candidate))
        for a,b in zip(r.dimensions(self.candidate),(470,700,930)):
            self.assertAlmostEqual(a,b,places=6)

    def test_front_datum_not_moved(self):
        a=r.by_name(self.base)['GGM_ShredRail']
        b=r.by_name(self.candidate)['GGM_ShredRail']
        self.assertLess(a.cut(b).Volume+b.cut(a).Volume,0.01)
        self.assertAlmostEqual(r.by_name(self.candidate)['GGM_SH_Spacer_90_100'].BoundBox.Center.y,100)

    def test_other_solids_only_rigidly_moved(self):
        before=[v for v in self.base if v['name']!='GGM_SH_Base']
        after=[v for v in self.candidate if v['name']!='GGM_SH_Base']
        self.assertEqual(r.check_preserved(before,after,self.transforms),len(before))

    def test_unmodified_plate_is_rejected(self):
        bad=self.copy(); legacy,_=r.placement(self.base)
        old=r.by_name(legacy)['GGM_SH_Base']
        for row in bad:
            if row['name']=='GGM_SH_Base': row['shape']=old
        with self.assertRaisesRegex(ValueError,'bolt hole'):
            check_mounts(self.base,bad)

    def test_floating_spacer_rejected(self):
        bad=self.copy(); r.by_name(bad)['GGM_SH_Spacer_90_100'].translate(App.Vector(0,0,0.1))
        with self.assertRaises(ValueError): check_mounts(self.base,bad)

    def test_floating_front_rail_rejected(self):
        bad=self.copy(); r.by_name(bad)['GGM_ShredRail'].translate(App.Vector(0,0,-0.1))
        with self.assertRaises(ValueError): check_mounts(self.base,bad)

    def test_collection_projection_preserved(self):
        self.assertGreaterEqual(min(r.check_collection(self.candidate)['inward_margins_mm']),5)

if __name__=='__main__': unittest.main()
