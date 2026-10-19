"""Element connectivity and force/moment checks independent of a solver run."""
import math
import sys
import unittest
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.compact_layout_v08.quadratic_mesh import exterior_faces
from analysis.compact_layout_v08.shelf_fea import deck


def fixture(variant):
    dx, dy = (0, 0) if variant == 'before' else (-18, 29)
    nodes, elements, centres = {}, [], []
    for x in (55, 248):
        for y in (233, 293):
            x, yy = x, y + dy
            xx = x + dx; centres.append((xx, yy))
            points = [np.array(v, dtype=float) for v in
                ((xx-5,yy-5,536),(xx+5,yy-5,536),(xx,yy+10,536),(xx,yy,530))]
            points += [(points[a]+points[b])/2 for a,b in
                       ((0,1),(1,2),(0,2),(0,3),(1,3),(2,3))]
            first = len(nodes)+1
            for i, point in enumerate(points):
                nodes[first+i] = tuple(point)
            elements.append(','.join(map(str, [len(elements)+1, *range(first,first+10)])))
    for x in (90, 220):
        for y in (100, 280):
            for angle in (0, 120, 240):
                theta = math.radians(angle)
                nodes[len(nodes)+1] = (x+3.3*math.cos(theta), y+3.3*math.sin(theta), 530)
    return nodes, elements, centres


class ShelfMeshTests(unittest.TestCase):
    def test_quadratic_faces_have_correct_edge_nodes(self):
        faces = exterior_faces(['1,1,2,3,4,5,6,7,8,9,10'])
        self.assertEqual(len(faces), 4)
        self.assertEqual(faces[0], (1,2,3,5,6,7))
        self.assertTrue(all(len(set(face)) == 6 for face in faces))

    def test_bad_connectivity_rejected(self):
        for values in ('1,1,2,3,4', '1,1,2,3,4,5,6,7,8,9,9'):
            with self.assertRaises(ValueError):
                exterior_faces([values])

    def test_uniform_patch_force_and_first_moment(self):
        for variant in ('before', 'after'):
            nodes, elements, centres = fixture(variant)
            for direction in (-1, 1):
                with self.subTest(variant=variant, direction=direction):
                    text, applied, fixed = deck(nodes, elements, variant, direction)
                    force = 100.0 * direction
                    expected = [force*sum(y for x,y in centres)/1000,
                                -force*sum(x for x,y in centres)/1000, 0]
                    np.testing.assert_allclose(applied['force_n'], [0,0,4*force], atol=1e-9)
                    np.testing.assert_allclose(applied['moment_nm'], expected, atol=1e-9)
                    self.assertEqual(len(fixed), 12)
                    np.testing.assert_allclose(applied['post_patch_areas_mm2'], [75]*4)
                    self.assertIn('TYPE=C3D10', text)
                    load = text.split('*CLOAD\n')[1].split('*NODE PRINT')[0]
                    loaded_ids = {int(line.split(',')[0]) for line in load.splitlines()}
                    corner_ids = {i+j for i in (1,11,21,31) for j in (0,1,2)}
                    self.assertTrue(loaded_ids.isdisjoint(corner_ids))

    def test_missing_support_nodes_rejected(self):
        nodes, elements, _ = fixture('before')
        with self.assertRaises(ValueError):
            deck({n:p for n,p in nodes.items() if n <= 40}, elements, 'before', -1)

    def test_missing_post_patch_rejected(self):
        nodes, elements, _ = fixture('before')
        with self.assertRaises(ValueError):
            deck(nodes, elements[:-1], 'before', -1)

    def test_invalid_variant_and_direction_rejected(self):
        nodes, elements, _ = fixture('before')
        for variant, direction in (('unknown',1),('before',0),('after',True)):
            with self.assertRaises(ValueError):
                deck(nodes, elements, variant, direction)


if __name__ == '__main__':
    unittest.main()
