"""Recommendation service responsible for deriving agronomic decisions."""

from smart_soil_analyzer.config.settings import AnalyzerThresholds
from smart_soil_analyzer.domain.models import CropRecommendation, SoilReading


class SoilRecommendationService:
    """Single-responsibility service for recommendation generation."""

    def __init__(self, thresholds: AnalyzerThresholds | None = None) -> None:
        self._thresholds = thresholds or AnalyzerThresholds()

    def analyze(self, reading: SoilReading) -> CropRecommendation:
        moisture_status = self._classify_moisture(reading.moisture_pct)
        salinity_risk = self._classify_salinity(reading.ec_ds_m)
        ph_status = self._classify_ph(reading.ph)
        irrigation_advice = self._irrigation_advice(moisture_status, salinity_risk)
        confidence = self._confidence(reading)

        return CropRecommendation(
            moisture_status=moisture_status,
            salinity_risk=salinity_risk,
            ph_status=ph_status,
            irrigation_advice=irrigation_advice,
            confidence_score=confidence,
        )

    def _classify_moisture(self, moisture_pct: float) -> str:
        if moisture_pct < self._thresholds.dry_moisture_cutoff:
            return "dry"
        if moisture_pct <= self._thresholds.optimal_moisture_ceiling:
            return "optimal"
        return "waterlogged"

    def _classify_salinity(self, ec_ds_m: float) -> str:
        if ec_ds_m >= self._thresholds.high_salinity_cutoff:
            return "high"
        if ec_ds_m >= self._thresholds.moderate_salinity_cutoff:
            return "moderate"
        return "low"

    def _classify_ph(self, ph: float | None) -> str:
        if ph is None:
            return "unknown"
        if ph < self._thresholds.ph_low_cutoff:
            return "acidic"
        if ph > self._thresholds.ph_high_cutoff:
            return "alkaline"
        return "balanced"

    def _irrigation_advice(self, moisture_status: str, salinity_risk: str) -> str:
        if moisture_status == "dry" and salinity_risk == "high":
            return "Irrigate lightly and schedule leaching irrigation within 48h."
        if moisture_status == "dry":
            return "Irrigate in the next cycle; monitor run-off efficiency."
        if moisture_status == "waterlogged":
            return "Pause irrigation and improve drainage aeration."
        return "Maintain current irrigation schedule."

    def _confidence(self, reading: SoilReading) -> float:
        # Confidence is penalized when pH is absent to surface data-quality uncertainty.
        return 0.95 if reading.ph is not None else 0.8
