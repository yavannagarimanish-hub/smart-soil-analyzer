"""Domain models that represent validated soil data and recommendations."""

from dataclasses import dataclass

from .exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class SoilReading:
    """Immutable soil reading captured from sensor inputs."""

    moisture_pct: float
    temperature_c: float
    ec_ds_m: float
    ph: float | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.moisture_pct <= 100:
            raise ValidationError("moisture_pct must be between 0 and 100")

        if not -30 <= self.temperature_c <= 80:
            raise ValidationError("temperature_c must be between -30 and 80 Celsius")

        if not 0 <= self.ec_ds_m <= 20:
            raise ValidationError("ec_ds_m must be between 0 and 20 dS/m")

        if self.ph is not None and not 0 <= self.ph <= 14:
            raise ValidationError("ph must be between 0 and 14")


@dataclass(frozen=True, slots=True)
class CropRecommendation:
    """Normalized recommendation output to power downstream UIs/APIs."""

    moisture_status: str
    salinity_risk: str
    ph_status: str
    irrigation_advice: str
    confidence_score: float

    def __post_init__(self) -> None:
        if not 0 <= self.confidence_score <= 1:
            raise ValidationError("confidence_score must be between 0 and 1")
