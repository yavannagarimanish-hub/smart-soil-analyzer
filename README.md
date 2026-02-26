# Smart Soil Analyzer

Production-ready baseline for an affordable soil intelligence system that turns raw sensor readings into actionable crop recommendations.

## Why this exists
Smart Soil Analyzer helps field teams and farm platforms quickly assess soil conditions using moisture, temperature, EC (salinity proxy), and optional pH readings.

## Features
- Clean architecture with clear separation of domain, services, interfaces, and configuration.
- Strict sensor validation to prevent unsafe assumptions.
- Deterministic recommendation engine with confidence scoring.
- CLI interface for easy integration with gateways, scripts, and edge devices.
- Test suite for critical agronomic logic and boundary validation.

## Project structure

```text
src/smart_soil_analyzer/
├── config/         # Thresholds and system configuration
├── domain/         # Core entities and validation rules
├── interfaces/     # CLI and future API adapters
├── services/       # Recommendation orchestration logic
└── main.py         # Entrypoint

tests/              # Unit tests
```

## Quick start

### 1) Install locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2) Run analyzer
```bash
soil-analyzer --moisture 33 --temperature 29 --ec 1.8 --ph 6.7
```

Example output:
```json
{
  "moisture_status": "optimal",
  "salinity_risk": "low",
  "ph_status": "balanced",
  "irrigation_advice": "Maintain current irrigation schedule.",
  "confidence_score": 0.95
}
```

### 3) Run tests
```bash
pytest
```

## Reliability and security notes
- Inputs are validated at the domain layer before analysis.
- Configuration is centralized for safer threshold tuning by geography/crop profile.
- No secrets are committed; service currently runs fully offline.

## Scalability roadmap
- Add API interface (`FastAPI`) in `interfaces/` without changing domain/service layers.
- Externalize thresholds per crop and region to a datastore.
- Add telemetry hooks for device health and drift monitoring.
- Introduce ML-assisted recommendation overrides with human-review mode.
