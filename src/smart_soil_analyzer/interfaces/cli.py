"""CLI adapter that separates presentation from domain/service logic."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from smart_soil_analyzer.domain.exceptions import ValidationError
from smart_soil_analyzer.domain.models import SoilReading
from smart_soil_analyzer.services.recommendation import SoilRecommendationService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="soil-analyzer",
        description="Analyze soil sensor readings and generate agronomic recommendations.",
    )
    parser.add_argument("--moisture", type=float, required=True, help="Soil moisture percentage")
    parser.add_argument("--temperature", type=float, required=True, help="Soil temperature in Celsius")
    parser.add_argument("--ec", type=float, required=True, help="Electrical conductivity in dS/m")
    parser.add_argument("--ph", type=float, help="Optional pH value")
    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        reading = SoilReading(
            moisture_pct=args.moisture,
            temperature_c=args.temperature,
            ec_ds_m=args.ec,
            ph=args.ph,
        )
    except ValidationError as error:
        parser.error(str(error))
        return 2

    recommendation = SoilRecommendationService().analyze(reading)
    print(json.dumps(asdict(recommendation), indent=2))
    return 0
