"""Canonical compact placement for the v0.8 integrated machine."""
from __future__ import annotations

import json
from pathlib import Path

import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "cad/parameters/compact_layout_v08.json"


def _by_name(rows):
    result = {row["name"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError("duplicate integrated object name")
    return result


def _move(shape, delta):
    result = shape.copy()
    result.translate(App.Vector(*delta))
    return result


def apply_compact_layout(items):
    spec = json.loads(CONTRACT.read_text())
    rows = [dict(row, shape=row["shape"].copy()) for row in items]
    original = _by_name(items)
    upper = tuple(spec["upper_translation_mm"])
    collector = tuple(spec["collector_translation_mm"])
    changed = []
    for row in rows:
        name = row["name"]
        if row["group"] in spec["front_process_groups"]:
            row["shape"] = _move(row["shape"], upper)
            changed.append(name)
        elif name == "FlakeBin" or name.startswith("PPR-C03"):
            row["shape"] = _move(row["shape"], collector)
            changed.append(name)

    fixed = set(spec["fixed_support_objects"])
    fixed.update(name for name in original if any(
        name.startswith(prefix) for prefix in spec["fixed_support_prefixes"]))
    by = _by_name(rows)
    for name in fixed:
        if name not in by:
            raise ValueError("compact support object missing: " + name)
        by[name]["shape"] = original[name]["shape"].copy()
        if name in changed:
            changed.remove(name)

    shelf_name = spec["shelf_object"]
    stock_box = by[shelf_name]["shape"].BoundBox
    plate = Part.makeBox(stock_box.XLength, stock_box.YLength, stock_box.ZLength,
                         App.Vector(stock_box.XMin, stock_box.YMin, stock_box.ZMin))
    holes = []
    for name, row in by.items():
        if name.startswith("GGM_SH_Spacer_"):
            diameter = 6.6
        elif name.startswith("GGM_SH_Post_"):
            diameter = 5.5
        else:
            continue
        box = row["shape"].BoundBox
        x, y = box.Center.x, box.Center.y
        margin = min(x-stock_box.XMin, stock_box.XMax-x,
                     y-stock_box.YMin, stock_box.YMax-y) - diameter/2
        if margin < 5.0:
            raise ValueError("compact shelf hole edge ligament: " + name)
        hole = Part.makeCylinder(diameter/2, stock_box.ZLength,
                                 App.Vector(x, y, stock_box.ZMin))
        plate = plate.cut(hole)
        holes.append((name, x, y, diameter))
    if len(holes) != 8 or not plate.isValid() or len(plate.Solids) != 1:
        raise ValueError("invalid compact eight-hole shelf")
    if abs(plate.Volume - original[shelf_name]["shape"].Volume) > 0.01:
        raise ValueError("compact shelf stock/hole volume drift")
    by[shelf_name]["shape"] = plate.removeSplitter()
    if shelf_name not in changed:
        changed.append(shelf_name)
    boxes = [row["shape"].BoundBox for row in rows]
    envelope = [max(getattr(box, axis+"Max") for box in boxes) -
                min(getattr(box, axis+"Min") for box in boxes) for axis in "XYZ"]
    if any(abs(value-target) > 1e-6 for value, target in zip(envelope, spec["envelope_mm"])):
        raise ValueError(f"compact envelope drift: {envelope}")
    for name, x, y, diameter in holes:
        shape = by[name]["shape"]
        box = shape.BoundBox
        if max(abs(box.Center.x-x), abs(box.Center.y-y)) > 1e-6:
            raise ValueError("compact shelf/mount axis drift: " + name)
        probe = Part.makeCylinder(diameter/2-0.005, plate.BoundBox.ZLength,
                                  App.Vector(x, y, plate.BoundBox.ZMin))
        if plate.common(probe).Volume > 0.01:
            raise ValueError("compact shelf mounting hole missing: " + name)
    return rows, sorted(set(changed))
