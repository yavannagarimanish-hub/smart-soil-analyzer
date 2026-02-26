"""Smart Soil Analyzer package."""

from .domain.models import CropRecommendation, SoilReading
from .services.recommendation import SoilRecommendationService

__all__ = ["CropRecommendation", "SoilReading", "SoilRecommendationService"]
