from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class CropProfile:
    n: Tuple[float, float]
    p: Tuple[float, float]
    k: Tuple[float, float]
    temp: Tuple[float, float]
    humidity: Tuple[float, float]
    ph: Tuple[float, float]
    rainfall: Tuple[float, float]
    base_yield: float
    market_price_per_ton: float
    base_cost_per_hectare: float


CROPS: Dict[str, CropProfile] = {
    "Rice": CropProfile((70, 120), (30, 60), (30, 55), (22, 34), (70, 90), (5.0, 6.8), (180, 320), 4.6, 22000.0, 36000.0),
    "Wheat": CropProfile((60, 110), (25, 55), (20, 45), (14, 27), (40, 65), (6.0, 7.8), (60, 140), 3.8, 24000.0, 32000.0),
    "Maize": CropProfile((65, 120), (30, 60), (25, 50), (18, 33), (50, 75), (5.5, 7.5), (80, 180), 5.2, 21000.0, 34000.0),
    "Cotton": CropProfile((70, 130), (25, 55), (30, 60), (21, 35), (45, 70), (5.8, 8.0), (70, 150), 2.3, 62000.0, 42000.0),
    "Sugarcane": CropProfile((100, 170), (40, 70), (40, 80), (20, 36), (55, 80), (6.0, 8.0), (120, 260), 68.0, 3400.0, 80000.0),
    "Soybean": CropProfile((40, 80), (35, 70), (20, 45), (19, 32), (45, 75), (6.0, 7.5), (70, 160), 2.8, 43000.0, 30000.0),
}


def _range_similarity(value: float, low: float, high: float) -> float:
    midpoint = (low + high) / 2
    spread = max((high - low) / 2, 1e-6)
    z = (value - midpoint) / spread
    return float(np.exp(-0.5 * z * z))


def quality_score(inputs: Dict[str, float], crop: str) -> float:
    p = CROPS[crop]
    sims = {
        "n": _range_similarity(inputs["N"], *p.n),
        "p": _range_similarity(inputs["P"], *p.p),
        "k": _range_similarity(inputs["K"], *p.k),
        "temp": _range_similarity(inputs["temperature"], *p.temp),
        "humidity": _range_similarity(inputs["humidity"], *p.humidity),
        "ph": _range_similarity(inputs["ph"], *p.ph),
        "rainfall": _range_similarity(inputs["rainfall"], *p.rainfall),
    }
    weights = {"n": 0.16, "p": 0.13, "k": 0.13, "temp": 0.16, "humidity": 0.14, "ph": 0.14, "rainfall": 0.14}
    score = sum(sims[k] * weights[k] for k in sims) * 100
    return round(float(np.clip(score, 0, 100)), 1)


def recommend_crop(inputs: Dict[str, float]) -> Tuple[str, Dict[str, float]]:
    scores = {crop: quality_score(inputs, crop) for crop in CROPS}
    best_crop = max(scores, key=scores.get)
    return best_crop, dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def estimate_yield(crop: str, quality: float, area_hectare: float) -> float:
    base = CROPS[crop].base_yield
    multiplier = 0.65 + (quality / 100.0) * 0.75
    return round(base * multiplier * area_hectare, 2)


def fertilizer_plan(crop: str, area_hectare: float, current_n: float, current_p: float, current_k: float) -> Dict[str, float]:
    profile = CROPS[crop]
    target_n = sum(profile.n) / 2
    target_p = sum(profile.p) / 2
    target_k = sum(profile.k) / 2

    req_n = max(target_n - current_n, 0) * area_hectare
    req_p = max(target_p - current_p, 0) * area_hectare
    req_k = max(target_k - current_k, 0) * area_hectare

    urea_kg = req_n / 0.46
    dap_kg = req_p / 0.46
    mop_kg = req_k / 0.6
    estimated_cost = (urea_kg * 6.5) + (dap_kg * 25.0) + (mop_kg * 17.0)

    return {
        "required_n_kg": round(req_n, 1),
        "required_p_kg": round(req_p, 1),
        "required_k_kg": round(req_k, 1),
        "urea_kg": round(urea_kg, 1),
        "dap_kg": round(dap_kg, 1),
        "mop_kg": round(mop_kg, 1),
        "estimated_cost": round(estimated_cost, 2),
    }


def irrigation_plan(crop: str, temp: float, humidity: float, rainfall_mm_week: float, area_hectare: float) -> Dict[str, float]:
    et0 = max(2.5, min(8.0, 0.15 * temp + 0.02 * (100 - humidity) + 2.0))
    kc = 1.15 if crop in {"Rice", "Sugarcane"} else 0.95
    weekly_demand_mm = et0 * kc * 7
    net_mm = max(weekly_demand_mm - rainfall_mm_week, 0)
    cubic_m = net_mm * 10 * area_hectare

    return {
        "weekly_demand_mm": round(weekly_demand_mm, 1),
        "rainfall_credit_mm": round(rainfall_mm_week, 1),
        "required_irrigation_mm": round(net_mm, 1),
        "required_irrigation_m3": round(cubic_m, 1),
    }


def profit_estimate(crop: str, estimated_yield_t: float, area_hectare: float, extra_cost: float = 0.0) -> Dict[str, float]:
    profile = CROPS[crop]
    revenue = estimated_yield_t * profile.market_price_per_ton
    base_cost = profile.base_cost_per_hectare * area_hectare
    total_cost = base_cost + extra_cost
    net = revenue - total_cost
    roi = (net / total_cost) * 100 if total_cost else 0.0
    breakeven_tons = total_cost / profile.market_price_per_ton

    return {
        "revenue": round(revenue, 2),
        "total_cost": round(total_cost, 2),
        "net_profit": round(net, 2),
        "roi_percent": round(roi, 1),
        "breakeven_tons": round(breakeven_tons, 2),
        "price_per_ton": profile.market_price_per_ton,
    }


def blend_datasets(left_df, right_df, left_weight: float = 0.5, right_weight: float = 0.5):
    common_cols = [column for column in left_df.columns if column in right_df.columns]
    numeric_cols = [column for column in common_cols if np.issubdtype(left_df[column].dtype, np.number) and np.issubdtype(right_df[column].dtype, np.number)]

    if not numeric_cols:
        return left_df.copy(), {"columns": [], "rows": int(len(left_df))}

    blend_rows = []
    left_total = max(left_weight + right_weight, 1e-9)
    left_factor = left_weight / left_total
    right_factor = right_weight / left_total

    for column in numeric_cols:
        blended_series = (left_df[column].fillna(0).astype(float) * left_factor) + (right_df[column].fillna(0).astype(float) * right_factor)
        blend_rows.append((column, round(float(blended_series.mean()), 3)))

    summary = {
        "columns": numeric_cols,
        "rows": int(min(len(left_df), len(right_df))),
        "blended_means": dict(blend_rows),
    }

    blended = left_df.copy()
    for column in numeric_cols:
        blended[column] = (left_df[column].fillna(0).astype(float) * left_factor) + (right_df[column].fillna(0).astype(float) * right_factor)

    return blended, summary


def disease_assessment(symptoms: Dict[str, float]) -> Dict[str, float | str | list]:
    yellowing = float(symptoms.get("yellowing", 0))
    spots = float(symptoms.get("spots", 0))
    wilting = float(symptoms.get("wilting", 0))
    holes = float(symptoms.get("holes", 0))
    mold = float(symptoms.get("mold", 0))
    crop = symptoms.get("crop", "Crop")

    fungal_score = spots * 0.3 + mold * 0.35 + wilting * 0.15 + yellowing * 0.1
    bacterial_score = wilting * 0.3 + yellowing * 0.25 + spots * 0.2 + mold * 0.15
    insect_score = holes * 0.4 + yellowing * 0.15 + wilting * 0.1 + spots * 0.1
    nutrient_score = yellowing * 0.45 + wilting * 0.2 + spots * 0.1

    candidates = {
        f"Fungal infection in {crop}": fungal_score,
        f"Bacterial stress in {crop}": bacterial_score,
        f"Insect damage in {crop}": insect_score,
        f"Nutrient deficiency in {crop}": nutrient_score,
    }
    diagnosis = max(candidates, key=candidates.get)
    confidence = round(float(np.clip(max(candidates.values()) * 10, 35, 99)), 1)

    recommendations = []
    if "Fungal" in diagnosis:
        recommendations.append("Improve airflow and consider a recommended fungicide program.")
    if "Bacterial" in diagnosis:
        recommendations.append("Remove badly affected leaves and avoid overhead watering.")
    if "Insect" in diagnosis:
        recommendations.append("Inspect undersides of leaves and use pest control if thresholds are exceeded.")
    if "Nutrient" in diagnosis:
        recommendations.append("Review fertilizer balance and soil test values before corrective action.")

    severity = round(float(np.clip(max(candidates.values()) / 10, 0, 10)), 1)
    return {
        "diagnosis": diagnosis,
        "confidence": confidence,
        "severity": severity,
        "recommendations": recommendations,
        "scores": {key: round(float(value), 2) for key, value in candidates.items()},
    }


def soil_health_score(soil: Dict[str, float]) -> Dict[str, float | str | list]:
    ph = float(soil.get("ph", 7.0))
    ec = float(soil.get("ec", 0.5))
    organic_carbon = float(soil.get("organic_carbon", 0.6))
    n = float(soil.get("n", 50.0))
    p = float(soil.get("p", 25.0))
    k = float(soil.get("k", 25.0))
    moisture = float(soil.get("moisture", 50.0))

    ph_score = 100 - min(abs(ph - 6.8) * 20, 60)
    ec_score = 100 - min(max(ec - 1.0, 0) * 40, 50)
    oc_score = min(organic_carbon * 100, 100)
    npk_score = (min(n / 2, 100) + min(p * 2, 100) + min(k * 2, 100)) / 3
    moisture_score = 100 - min(abs(moisture - 55) * 1.2, 50)

    overall = round(float(np.clip((ph_score * 0.22) + (ec_score * 0.16) + (oc_score * 0.22) + (npk_score * 0.25) + (moisture_score * 0.15), 0, 100)), 1)
    if overall >= 80:
        status = "Healthy"
    elif overall >= 60:
        status = "Moderate"
    else:
        status = "Needs Improvement"

    advice = []
    if ph < 6.0:
        advice.append("Soil is acidic. Consider lime-based correction.")
    elif ph > 7.8:
        advice.append("Soil is alkaline. Add organic matter and monitor micronutrients.")

    if ec > 1.5:
        advice.append("Electrical conductivity is elevated. Reduce salinity buildup and improve leaching.")
    if organic_carbon < 0.5:
        advice.append("Organic carbon is low. Add compost or farmyard manure.")
    if n < 40 or p < 20 or k < 20:
        advice.append("NPK values are below ideal range. Run fertilizer planning before sowing.")
    if moisture < 35:
        advice.append("Soil moisture is low. Improve irrigation timing and residue cover.")

    return {
        "overall_score": overall,
        "status": status,
        "ph_score": round(float(ph_score), 1),
        "ec_score": round(float(ec_score), 1),
        "organic_carbon_score": round(float(oc_score), 1),
        "npk_score": round(float(npk_score), 1),
        "moisture_score": round(float(moisture_score), 1),
        "advice": advice,
    }
