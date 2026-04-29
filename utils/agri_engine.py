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
