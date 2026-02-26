"""Application entrypoint."""

from smart_soil_analyzer.interfaces.cli import run_cli


def main() -> int:
    return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
