from smart_soil_analyzer.domain.exceptions import ValidationError
from smart_soil_analyzer.domain.models import SoilReading
from smart_soil_analyzer.services.recommendation import SoilRecommendationService


def test_analyze_dry_high_salinity() -> None:
    service = SoilRecommendationService()
    reading = SoilReading(moisture_pct=15, temperature_c=31, ec_ds_m=4.8, ph=8.2)

    result = service.analyze(reading)

    assert result.moisture_status == "dry"
    assert result.salinity_risk == "high"
    assert result.ph_status == "alkaline"
    assert "leaching irrigation" in result.irrigation_advice
    assert result.confidence_score == 0.95


def test_analyze_without_ph_reduces_confidence() -> None:
    service = SoilRecommendationService()
    reading = SoilReading(moisture_pct=40, temperature_c=25, ec_ds_m=1.1)

    result = service.analyze(reading)

    assert result.moisture_status == "optimal"
    assert result.ph_status == "unknown"
    assert result.confidence_score == 0.8


def test_invalid_reading_raises_validation_error() -> None:
    try:
        SoilReading(moisture_pct=120, temperature_c=24, ec_ds_m=1.3)
    except ValidationError:
        assert True
        return

    assert False, "Expected ValidationError for out-of-range moisture"
