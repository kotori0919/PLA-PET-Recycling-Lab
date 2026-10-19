"""Ensure the canonical GGM assembly equals the reviewed 470x700x930 layout."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'cad/freecad/drive_v08')]
from cad.freecad.final_v08.generate import final_objects
from cad.freecad.drive_v08.assembly import integrated_objects
from analysis.compact_layout_v08.fixed_foot_layout import candidate, validate
from analysis.compact_layout_v08.review import by_name, dimensions
from validation.integrated_assembly_clearance import audit


class CanonicalCompactLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference, _ = integrated_objects(final_objects(), compact_layout=False)
        cls.expected, _, _ = candidate(cls.reference)
        cls.actual, _ = integrated_objects(final_objects())
        cls.spec = json.loads((ROOT/'cad/parameters/compact_layout_v08.json').read_text())

    def test_envelope_and_object_identity(self):
        self.assertEqual(set(by_name(self.actual)), set(by_name(self.reference)))
        for value, target in zip(dimensions(self.actual), self.spec['envelope_mm']):
            self.assertAlmostEqual(value, target, places=6)
    def test_exactly_matches_reviewed_fixed_foot_candidate(self):
        expected, actual = by_name(self.expected), by_name(self.actual)
        self.assertEqual(set(expected), set(actual))
        for name in expected:
            missing = expected[name].cut(actual[name]).Volume
            added = actual[name].cut(expected[name]).Volume
            self.assertLessEqual(max(missing, added), 0.01, name)

    def test_review_support_contract_still_holds(self):
        expected, transforms, holes = candidate(self.reference)
        result = validate(self.reference, expected, transforms, holes)
        self.assertEqual([round(v, 6) for v in result['dimensions_mm']], [470,700,930])

    def test_no_new_unclassified_collision(self):
        result = audit(self.actual)
        self.assertEqual(result['unexpected_count'], 0)

    def test_contract_is_fail_closed(self):
        self.assertEqual(self.spec['state'], 'CANONICAL_COMPACT_LAYOUT')
        self.assertTrue(self.spec['no_added_profiles'])
        self.assertTrue(self.spec['no_added_actuators'])
        self.assertFalse(self.spec['fabrication_authorized'])
        self.assertFalse(self.spec['energization_authorized'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
