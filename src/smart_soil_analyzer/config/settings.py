"""Centralized, typed application configuration."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalyzerThresholds:
    """Domain thresholds kept configurable for regional calibration."""

    dry_moisture_cutoff: float = 25.0
    optimal_moisture_floor: float = 25.0
    optimal_moisture_ceiling: float = 60.0
    high_salinity_cutoff: float = 4.0
    moderate_salinity_cutoff: float = 2.0
    ph_low_cutoff: float = 5.8
    ph_high_cutoff: float = 7.8
