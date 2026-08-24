from __future__ import annotations

import json
from pathlib import Path

import pytest

from cyrisk_controls.cli import main

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_control_comparison.json"


def test_cli_emits_non_causal_comparison(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["compare", str(FIXTURE)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["non_causal"] is True
    assert output["central_delta"] == "70000"


def test_cli_rejects_invalid_json(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text("not-json", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["compare", str(invalid)])
