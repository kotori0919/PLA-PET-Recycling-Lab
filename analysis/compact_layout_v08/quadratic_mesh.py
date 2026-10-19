"""Quadratic tetrahedral shelf mesh; surface traction uses consistent weights."""
from collections import defaultdict
from pathlib import Path
import math
import shutil
from analysis.final_validation.run_calculix_v08 import run, ROOT


def mesh_step(step, folder, size_mm):
    if not math.isfinite(size_mm) or size_mm <= 0:
        raise ValueError('positive mesh size required')
    output = folder/'gmsh.inp'
    log = run([shutil.which('gmsh') or 'gmsh', str(step), '-3', '-order', '2',
        '-format', 'inp', '-setnumber', 'Mesh.CharacteristicLengthMin', str(size_mm*0.55),
        '-setnumber', 'Mesh.CharacteristicLengthMax', str(size_mm), '-o', str(output)],
        ROOT, folder/'gmsh.log')
    if 'No ill-shaped tets' not in log:
        raise ValueError('mesh quality confirmation missing')
    return output


def read_gmsh_inp(path):
    nodes, elements, section = {}, [], ''
    for raw in Path(path).read_text().splitlines():
        line = raw.strip()
        if line.startswith('*'):
            section = 'nodes' if line.upper() == '*NODE' else (
                'elements' if 'TYPE=C3D10' in line.upper() else '')
            continue
        if not line or not section:
            continue
        values = [v.strip() for v in line.split(',')]
        if section == 'nodes':
            nodes[int(values[0])] = tuple(float(v) for v in values[1:4])
        else:
            if len(values) != 11 or len(set(values[1:])) != 10:
                raise ValueError('nondegenerate C3D10 connectivity required')
            elements.append(','.join(values))
    if not nodes or not elements:
        raise ValueError('missing quadratic volume mesh')
    return nodes, elements


def exterior_faces(elements):
    faces = defaultdict(list)
    mids = {(0,1):4, (1,2):5, (0,2):6, (0,3):7, (1,3):8, (2,3):9}
    for line in elements:
        values = [int(v) for v in line.split(',')]
        if len(values) != 11 or len(set(values[1:])) != 10:
            raise ValueError('nondegenerate C3D10 connectivity required')
        tet = values[1:]
        for ids in ((0,1,2), (0,3,1), (1,3,2), (2,3,0)):
            edge_ids = [mids[tuple(sorted(edge))] for edge in
                        ((ids[0],ids[1]), (ids[1],ids[2]), (ids[2],ids[0]))]
            face = tuple(tet[i] for i in (*ids, *edge_ids))
            faces[tuple(sorted(face[:3]))].append(face)
    if any(len(group) > 2 for group in faces.values()):
        raise ValueError('nonmanifold quadratic mesh')
    return [group[0] for group in faces.values() if len(group) == 1]
