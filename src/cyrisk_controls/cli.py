"""Local CLI for deterministic Cyrisk Controls comparisons."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from cyrisk_controls.engine import compare
from cyrisk_controls.models import ComparisonRequest


def main(argv: Sequence[str] | None = None) -> int:
    """Compare one local JSON request and emit stable JSON."""
    parser = argparse.ArgumentParser(prog="cyrisk-controls")
    parser.add_argument("command", choices=("compare",))
    parser.add_argument("request", type=Path)
    args = parser.parse_args(argv)
    try:
        request = ComparisonRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
        result = compare(request)
    except (OSError, ValidationError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(result.model_dump_json())
    return 0
