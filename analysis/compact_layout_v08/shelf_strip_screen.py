#!/usr/bin/env python3
"""Conservative strip screen for the compact shredder shelf relocation."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEOMETRY = ROOT / "analysis/compact_layout_v08/results/fixed_foot_geometry.json"
OUT = ROOT / "analysis/compact_layout_v08/results/shelf_strip_screen.json"
E_MPA = 200000.0
YIELD_MPA = 275.0
THICKNESS_MM = 6.0
STRIP_WIDTH_MM = 20.0
COMPARISON_LOAD_N = 100.0
REQUIRED_SF = 2.0


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def beam_case(load_xy, support_xy, force_n=COMPARISON_LOAD_N):
    length = math.dist(load_xy, support_xy)
    inertia = STRIP_WIDTH_MM * THICKNESS_MM**3 / 12.0
    moment = force_n * length
    stress = 6.0 * moment / (STRIP_WIDTH_MM * THICKNESS_MM**2)
    deflection = force_n * length**3 / (3.0 * E_MPA * inertia)
    capacity = YIELD_MPA * STRIP_WIDTH_MM * THICKNESS_MM**2 / (6.0 * length * REQUIRED_SF)
    return {"length_mm": length, "moment_nmm": moment, "stress_mpa": stress,
            "deflection_mm": deflection, "yield_sf": YIELD_MPA/stress,
            "per_post_load_limit_n_at_sf2": capacity}

def main() -> None:
    data = json.loads(GEOMETRY.read_text())
    holes = data["hole_schedule"]
    supports = [(row["x_mm"], row["y_mm"]) for row in holes
                if row["mating_object"].startswith("GGM_SH_Spacer_")]
    loads = [(row["mating_object"], (row["x_mm"], row["y_mm"])) for row in holes
             if row["mating_object"].startswith("GGM_SH_Post_")]
    if len(supports) != 4 or len(loads) != 4:
        raise ValueError("expected four shelf supports and four load posts")
    cases = []
    for name, point in loads:
        support = min(supports, key=lambda value: math.dist(point, value))
        row = beam_case(point, support)
        row.update(load_object=name, load_xy_mm=list(point), support_xy_mm=list(support))
        cases.append(row)
    worst = max(cases, key=lambda row: row["stress_mpa"])
    source_current = all((ROOT/path).is_file() and sha(ROOT/path) == digest
                         for path, digest in data.get("source_sha256", {}).items())
    checks = {
        "four_post_cases": len(cases) == 4,
        "comparison_load_yield_sf_ge_2": min(row["yield_sf"] for row in cases) >= REQUIRED_SF,
        "comparison_deflection_le_0p5mm": max(row["deflection_mm"] for row in cases) <= 0.5,
        "geometry_is_current": source_current and data.get("status") == "FIXED_FOOT_LAYOUT_GEOMETRY_PASS",
    }
    result = {"status": "COMPACT_SHELF_STRIP_SCREEN_PASS" if all(checks.values()) else "FAIL",
              "method": "independent 20 mm wide cantilever strip per post; ignores beneficial two-way plate action",
              "comparison_load_per_post_n": COMPARISON_LOAD_N, "checks": checks,
              "cases": cases, "worst_case": worst,
              "physical_validation_state": "NOT_RUN", "fabrication_authorized": False,
              "strength_qualified": False,
              "source_sha256": {str(Path(__file__).resolve().relative_to(ROOT)): sha(Path(__file__).resolve()),
                                str(GEOMETRY.relative_to(ROOT)): sha(GEOMETRY)},
              "limitations": ["100 N per post is a digital comparison load, not a measured operating load.",
                              "Strip model ignores beneficial two-way plate action and load sharing.",
                              "Bolt preload, slip, vibration, fatigue and received material remain physical gates.",
                              "The nonconverged C3D10 shelf study remains diagnostic and is not relabeled PASS."]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(result["status"], worst)
    if result["status"] != "COMPACT_SHELF_STRIP_SCREEN_PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
