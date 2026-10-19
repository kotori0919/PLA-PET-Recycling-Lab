"""Compare current and inset support positions; software-only, no machine control."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.frame_v08.beam_screen import model, benchmark


def crossrail_response(points_mm, forces_n, elements=32):
    points = np.asarray(points_mm, dtype=float)
    forces = np.asarray(forces_n, dtype=float)
    if (points.shape != (2,) or forces.shape != (2,) or not np.isfinite(points).all()
            or not np.isfinite(forces).all() or not 20 < points[0] < points[1] < 450
            or min(forces) < 0 or sum(forces) <= 0 or elements < 4):
        raise ValueError('invalid crossrail load positions or forces')
    x = np.unique(np.r_[np.linspace(20, 450, elements + 1), points])
    size = 2 * len(x)
    k, f = np.zeros((size, size)), np.zeros(size)
    ei = 69000.0 * 51400.0
    for i, length in enumerate(np.diff(x)):
        dofs = np.arange(2*i, 2*i+4)
        l = length
        ke = ei/l**3 * np.array([[12,6*l,-12,6*l], [6*l,4*l*l,-6*l,2*l*l],
                                [-12,-6*l,12,-6*l], [6*l,2*l*l,-6*l,4*l*l]])
        k[np.ix_(dofs, dofs)] += ke
    loaded = [int(np.argmin(abs(x - p))) for p in points]
    for node, force in zip(loaded, forces):
        f[2*node] -= force
    fixed = [0, size-2]
    free = np.setdiff1d(np.arange(size), fixed)
    u = np.zeros(size)
    u[free] = np.linalg.solve(k[np.ix_(free, free)], f[free])
    reaction = k @ u - f
    expected = np.array([sum(forces*(450-points))/430,
                         sum(forces*(points-20))/430])
    moments = expected[0]*(x-20)
    for p, force in zip(points, forces):
        moments -= force*np.maximum(x-p, 0)
    error = float(max(abs(reaction[fixed]-expected)))
    if error > 1e-5:
        raise ValueError('crossrail force/moment equilibrium failure')
    return {'points_mm': points.tolist(), 'forces_n': forces.tolist(),
            'support_reactions_n': reaction[fixed].tolist(), 'reaction_error_n': error,
            'max_deflection_mm': float(max(abs(u[::2]))),
            'max_bending_moment_nmm': float(max(abs(moments))),
            'work_nmm': float(f @ u), 'elements': len(x)-1}


def frame_rows(items):
    from analysis.frame_v08.audit_geometry import profiles, contacts
    from cad.freecad.drive_v08.frame_revision import steel_tie, CONTRACT
    spec = json.loads(CONTRACT.read_text())['tie']
    tie, section = steel_tie(spec)
    b = tie.BoundBox
    rows = profiles(items)
    rows.append({'id': spec['object'], 'source_object': spec['object'], 'axis': 0,
        'length_mm': spec['length_mm'],
        'box': [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],
        'section_properties': {'area_mm2': section.Area,
            'iy_mm4': section.MatrixOfInertia.A22, 'iz_mm4': section.MatrixOfInertia.A33,
            'j_mm4': section.Area*spec['thickness_mm']**2/3, 'e_mpa': 200000,
            'centroid_yz_mm': [section.CenterOfMass.y, section.CenterOfMass.z]}})
    return contacts(rows, items)


def main():
    from analysis.compact_layout_v08.review import placement, CONTRACT, by_name
    from cad.freecad.final_v08.generate import final_objects
    from cad.freecad.drive_v08.assembly import integrated_objects
    from validation.integrated_assembly_clearance import geometry_source_paths
    contract = ROOT/'cad/parameters/ggm_frame_revision.json'
    paths = geometry_source_paths()+[Path(__file__).resolve(), CONTRACT, contract,
        ROOT/'analysis/compact_layout_v08/review.py', ROOT/'analysis/frame_v08/beam_screen.py',
        ROOT/'analysis/frame_v08/audit_geometry.py',
        ROOT/'analysis/compact_layout_v08/support_datum.py']
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    config = json.loads(CONTRACT.read_text())
    base, _ = integrated_objects(final_objects(), compact_layout=False)
    from analysis.compact_layout_v08.support_datum import proposal
    candidate, _ = proposal(base)
    a, b = frame_rows(base), frame_rows(candidate)
    same = {(r['id'], r['length_mm']) for r in a} == {(r['id'], r['length_mm']) for r in b}
    if not same:
        raise ValueError('frame identity or cut length changed')
    unit = benchmark()
    rows = []
    for torsion in (0.03, 0.1, 1.0):
        for joint in (0.01, 1.0, 100.0):
            before, after = model(a, torsion, joint), model(b, torsion, joint)
            ratio = np.array(after['compliance_mm']) / np.array(before['compliance_mm'])
            rows.append({'torsion_fraction': torsion, 'joint_scale': joint,
                'max_compliance_ratio': float(max(ratio)),
                'worst_case': before['labels'][int(np.argmax(ratio))],
                'before': before, 'after': after})
    local = []
    for y in (100, 280):
        names = [f'GGM_SH_Spacer_{x}_{y}' for x in (90, 220)]
        xp = [[by_name(items)[name].BoundBox.Center.x for name in names]
              for items in (base, candidate)]
        for fraction in (0.25, 0.5, 0.75):
            forces = [100*fraction, 100*(1-fraction)]
            before, after = [crossrail_response(p, forces) for p in xp]
            fine = crossrail_response(xp[1], forces, 64)
            local.append({'spacer_row_y_mm': y, 'left_load_fraction': fraction,
                'before': before, 'after': after,
                'work_ratio': after['work_nmm']/before['work_nmm'],
                'mesh_relative_change': abs(fine['max_deflection_mm']/after['max_deflection_mm']-1)})
    contract = ROOT/'cad/parameters/ggm_frame_revision.json'
    limit = json.loads(contract.read_text())['comparative_screen_limit_ratio']
    checks = {'frame_identity_and_cut_lengths_preserved': same,
        'global_compliance_ratio': max(r['max_compliance_ratio'] for r in rows) <= limit,
        'local_load_point_compliance_ratio': max(r['work_ratio'] for r in local) <= limit,
        'local_refinement': max(r['mesh_relative_change'] for r in local) <= 0.01}
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h for p,h in source_hashes.items()):
        raise ValueError('source changed during frame comparison')
    result = {'status': 'COMPACT_FRAME_RESPONSE_PASS' if all(checks.values()) else 'REVIEW_FAIL',
        'checks': checks, 'limit_ratio': limit, 'benchmark': unit, 'configurations': rows,
        'crossrail_load_cases': local, 'cases_per_configuration': 27,
        'source_sha256': source_hashes,
        'physical_validation_state': 'NOT_RUN', 'fabrication_authorized': False,
        'canonical_geometry_promoted': False,
        'scope': 'Same frame and material assumptions; moved rail unit loads and actual spacer X positions',
        'limitations': ['Linear elastic nominal sections; no measured T-slot or joint stiffness.',
            '27 unit-force cases at rail centres per stiffness configuration, not machine operating loads.',
            'Two simply-supported local loads explore distribution, not a measured motor load split.',
            'No joint slip, bolt preload, dynamic response, fatigue or local bracket qualification.']}
    out = Path(__file__).with_name('results')/'frame_response.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(result['status'], json.dumps({'checks': checks,
        'worst_frame_ratio': max(r['max_compliance_ratio'] for r in rows),
        'worst_spacer_ratio': max(r['work_ratio'] for r in local)}), flush=True)
    if not all(checks.values()):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
