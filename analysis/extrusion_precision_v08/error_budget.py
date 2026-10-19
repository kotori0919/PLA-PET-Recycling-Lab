#!/usr/bin/env python3
"""Filament diameter error budget from mass conservation; screening, not a process model.

d = sqrt(4 Q / (pi rho v)) for melt mass flow Q, solid density rho and puller linear speed v.
Material densities are literature-class assumptions (INFERRED) and are labelled as such; the
conclusions below only use ratios, so they are insensitive to the exact density.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis/extrusion_precision_v08/results/error_budget.json"

D = 1.75                  # mm, nominal filament diameter (cad/parameters/baseline.json forming.target_diameter_mm)
TOL = 0.05                # mm, individual-sample band
SIGMA_LIMIT = 0.015       # mm, proposed consistency limit (U95 0.03 / 2)
DIE_TO_GAUGE_MM = 248.0   # cad/parameters/baseline.json forming.die_to_gauge_mm
DIE_TO_PULLER_MM = 323.0  # forming.straight_length_die_to_puller_mm
ROLLER_OD_MM = 40.0       # forming.puller_roller_od_mm
SLIP_LIMIT = 0.01         # P12 contract: puller slip + U95 <= 1 %
THROUGHPUT_G_H = {"PLA": 99.4, "PET": 97.5}   # calculations/screw_sensitivity.md nominal at profile rpm
DENSITY_G_CM3 = {"PLA": 1.24, "PET": 1.33}    # INFERRED literature values
FEEDER_RANGE_G_H = (95.858, 101.310)          # analysis/process_feed/feed_validation.json
RESIDENCE_S = (84.0, 160.3)                   # calculations/screw_sensitivity.md low-nominal-high span
LEAK_REL_PER_0P01_RADIAL = 0.0146             # calculations/screw_sensitivity.md: 0.15->0.16 mm radial, PLA


def relative_diameter(d_flow, d_speed):
    """First-order relative diameter change from relative flow and puller speed changes."""
    return 0.5 * (d_flow - d_speed)


def main():
    area = math.pi * D * D / 4.0
    rel_band = TOL / D                      # +/- relative diameter for the individual band
    rel_sigma = SIGMA_LIMIT / D
    result = {
        "status": "ERROR_BUDGET_SCREEN_NOT_A_PROCESS_VALIDATION",
        "basis": "mass conservation; first-order; densities INFERRED; no die-swell or rheology model",
        "diameter_mm": D,
        "relative_diameter_individual_band": rel_band,
        "relative_diameter_sigma_limit": rel_sigma,
        # d ~ sqrt(Q/v): a relative change in Q or v moves d by half of it
        "allowed_combined_flow_speed_variation_individual": 2 * rel_band,
        "allowed_combined_flow_speed_variation_sigma": 2 * rel_sigma,
        "per_unit_diameter_sensitivity_mm_per_percent": D * 0.5 * 0.01,
        "materials": {},
    }
    for mat, q in THROUGHPUT_G_H.items():
        vol = q / 3600.0 / (DENSITY_G_CM3[mat] * 1e-3)    # mm^3/s
        v = vol / area                                    # mm/s
        rpm = v / (math.pi * ROLLER_OD_MM) * 60.0
        result["materials"][mat] = {
            "throughput_g_h": q, "volume_flow_mm3_s": vol, "filament_speed_mm_s": v,
            "puller_roller_rpm": rpm,
            "transport_delay_to_gauge_s": DIE_TO_GAUGE_MM / v,
            "transport_delay_to_puller_s": DIE_TO_PULLER_MM / v,
        }
    # Puller slip: slip variation moves speed one-for-one, diameter by half of it.
    result["puller_slip_limit_diameter_effect_mm"] = D * 0.5 * SLIP_LIMIT
    result["puller_slip_limit_share_of_individual_band"] = D * 0.5 * SLIP_LIMIT / TOL
    # Roller eccentricity e gives a peak speed ripple e/R (surface-speed change per revolution).
    radius = ROLLER_OD_MM / 2.0
    ripple_allow = 0.005                                  # 0.5 % speed ripple (PROPOSED allocation)
    result["roller_runout"] = {
        "speed_ripple_allocation": ripple_allow,
        "max_eccentricity_mm": ripple_allow * radius,
        "max_tir_mm": 2 * ripple_allow * radius,
        "diameter_effect_mm": D * 0.5 * ripple_allow,
    }
    # Feeder-only flow spread across the 40 surrogate cases (level differences, not a time series).
    mid = sum(FEEDER_RANGE_G_H) / 2.0
    half = (FEEDER_RANGE_G_H[1] - FEEDER_RANGE_G_H[0]) / 2.0 / mid
    result["feeder_flow_halfband_relative"] = half
    result["feeder_flow_halfband_diameter_mm_if_uncorrected"] = D * 0.5 * half
    result["feeder_share_of_individual_band_if_uncorrected"] = D * 0.5 * half / TOL
    # First-order lag of the melt path (residence time constant) attenuates fast pulsation.
    tau = sum(RESIDENCE_S) / 2.0
    attenuation = {str(T): 1.0 / math.sqrt(1.0 + (2 * math.pi * tau / T) ** 2) for T in (5, 10, 30, 120, 600)}
    result["melt_path_lag_attenuation_by_period_s"] = {"tau_s": tau, "gain": attenuation,
        "note": "tau taken as mean residence; INFERRED, not a measured transfer function"}
    # Static part-to-part throughput error is removed by the diameter loop; wear drift is slow.
    result["clearance_effect"] = {
        "throughput_change_per_0p01_mm_radial": LEAK_REL_PER_0P01_RADIAL,
        "diameter_change_mm_per_0p01_mm_radial": D * 0.5 * LEAK_REL_PER_0P01_RADIAL,
        "note": "static offset; corrected by the puller setpoint, matters as slow wear drift",
    }
    # Feedback bandwidth: the loop cannot reject disturbances faster than roughly 1/(4 delay).
    delay = result["materials"]["PLA"]["transport_delay_to_gauge_s"]
    result["feedback_limit"] = {
        "gauge_delay_s_PLA": delay,
        "disturbance_period_unrejectable_below_s": 4 * delay,
        "note": "rule of thumb for a pure-delay loop; disturbances shorter than this must be limited at the source",
    }
    result["requirements_derived"] = [
        {"id": "XP-01", "text": "Reference diameter instrument independent of the machine gauge, resolution <=0.001 mm, "
         "MSA %GRR <=10 % of the 0.10 mm individual band (<=0.01 mm) before P10", "basis": "REFERENCE_U95 0.01 mm"},
        {"id": "XP-02", "text": "Puller roller radial runout TIR <= %.2f mm measured by dial indicator before P12"
         % result["roller_runout"]["max_tir_mm"], "basis": "0.5 % speed ripple allocation"},
        {"id": "XP-03", "text": "Puller slip variation over the stable window <=0.5 % (half of the 1 % maximum)", "basis": "slip share of band"},
        {"id": "XP-04", "text": "Record feeder, screw current and puller speed at >=1 Hz during P10-P12 to separate "
         "disturbance periods shorter and longer than %.0f s" % result["feedback_limit"]["disturbance_period_unrejectable_below_s"],
         "basis": "feedback limit"},
        {"id": "XP-06", "text": "Puller speed estimate must resolve 0.25 %% at %.1f-%.1f rpm; tach pulses per revolution is a calibration "
         "value today (OPEN): confirm the achieved resolution on the real tach, otherwise add a roller encoder or period-timer capture"
         % (result["materials"]["PET"]["puller_roller_rpm"], result["materials"]["PLA"]["puller_roller_rpm"]), "basis": "low roller speed"},
        {"id": "XP-05", "text": "Screw flight OD and barrel ID measured before P6; track radial clearance each cleaning cycle",
         "basis": "clearance drift"},
    ]
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("EXTRUSION_ERROR_BUDGET_SCREEN", json.dumps({
        "allowed_flow_speed_variation_sigma": result["allowed_combined_flow_speed_variation_sigma"],
        "gauge_delay_s_PLA": delay, "roller_max_tir_mm": result["roller_runout"]["max_tir_mm"],
        "slip_share": result["puller_slip_limit_share_of_individual_band"],
        "feeder_share": result["feeder_share_of_individual_band_if_uncorrected"]}))


if __name__ == "__main__":
    main()
