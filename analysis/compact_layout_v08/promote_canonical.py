#!/usr/bin/env python3
"""Bind the reviewed 470x700x930 layout to the canonical CAD contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "analysis/compact_layout_v08/results"
OUT = RESULTS / "canonical_promotion.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((RESULTS/name).read_text())


def current(data: dict) -> bool:
    hashes = data.get("source_sha256", {})
    return bool(hashes) and all((ROOT/p).is_file() and sha(ROOT/p) == digest for p,digest in hashes.items())


def main() -> None:
    contract = json.loads((ROOT/"cad/parameters/compact_layout_v08.json").read_text())
    review = load("review.json")
    fixed = load("fixed_foot_geometry.json")
    support = load("support_datum.json")
    frame = load("frame_response.json")
    strip = load("shelf_strip_screen.json")
    tetra = load("shelf_fea.json")
    checks = {
        "canonical_contract": contract.get("state") == "CANONICAL_COMPACT_LAYOUT",
        "preferred_envelope": contract.get("envelope_mm") == [470.0,700.0,930.0],
        "review_geometry": review.get("status") == "COMPACT_PLACEMENT_GEOMETRY_REVIEW_PASS" and current(review),
        "fixed_supports_and_shelf": fixed.get("status") == "FIXED_FOOT_LAYOUT_GEOMETRY_PASS" and current(fixed),
        "support_datum": support.get("status") == "COMPACT_SUPPORT_DATUM_REVIEW_PASS" and current(support),
        "frame_response": frame.get("status") == "COMPACT_FRAME_RESPONSE_PASS" and current(frame) and all(frame.get("checks",{}).values()),
        "conservative_shelf_strip": strip.get("status") == "COMPACT_SHELF_STRIP_SCREEN_PASS" and current(strip) and all(strip.get("checks",{}).values()),
        "nonconverged_tetra_not_promoted": tetra.get("status") == "FAIL" and tetra.get("checks",{}).get("all_solver_pass") is True and tetra.get("checks",{}).get("displacement_convergence") is False,
        "no_size_driven_power_or_profile_addition": contract.get("no_added_profiles") is True and contract.get("no_added_actuators") is True and contract.get("no_heater_or_psu_upsizing") is True,
    }
    status = "COMPACT_CANONICAL_DIGITAL_PROMOTION_PASS" if all(checks.values()) else "FAIL"
    report = {
        "schema_version": 1,
        "status": status,
        "purpose": contract["purpose"],
        "canonical_envelope_mm": contract["envelope_mm"],
        "volume_reduction_from_470x729x930_fraction": 1.0 - 700.0/729.0,
        "checks": checks,
        "physical_validation_state": "NOT_RUN",
        "fabrication_authorized": False,
        "energization_authorized": False,
        "strength_scope": "relative frame response plus conservative 100 N/post strip screen; not measured operating loads",
        "diagnostic_not_accepted": {
            "file": "analysis/compact_layout_v08/results/shelf_fea.json",
            "status": tetra.get("status"),
            "reason": "C3D10/C3D4 local shelf displacement did not meet mesh-convergence criterion; retained as diagnostic, never relabeled PASS"
        },
        "physical_inputs_still_required": [
            "received GGM mass/mount dimensions and actual fastener engagement",
            "P2 frame stock/kerf and assembled squareness",
            "P3 operating/jam load observations and vibration",
            "physical service-access and guard checks"
        ],
    }
    sources = [Path(__file__).resolve(), ROOT/"cad/parameters/compact_layout_v08.json",
               ROOT/"cad/freecad/drive_v08/compact_layout.py", ROOT/"cad/freecad/drive_v08/assembly.py",
               *(RESULTS/name for name in ("review.json","fixed_foot_geometry.json","support_datum.json",
                                            "frame_response.json","shelf_strip_screen.json","shelf_fea.json"))]
    report["source_sha256"] = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    print(status, report["canonical_envelope_mm"], checks)
    if status != "COMPACT_CANONICAL_DIGITAL_PROMOTION_PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
