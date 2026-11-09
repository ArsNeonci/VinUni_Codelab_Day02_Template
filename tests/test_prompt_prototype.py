"""Nhóm A95 - offline regression tests, not live model evaluations.
Chu Quang Linh <Quanglinh1286@gmail.com>; Nguyễn Minh Quân <minhquandhtb@gmail.com>;
Trương Thu Hà <thuha261102@gmail.com>; Phan Trần Mạnh Cường <manhcuong2005.28@gmail.com>;
Nguyễn Lương Phúc <luongphuc.lpu@gmail.com>.
"""

import importlib.util
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

SPEC = importlib.util.spec_from_file_location(
    "prompt_prototype", Path(__file__).resolve().parents[1] / "starter-code/prompt_prototype.py"
)
prototype = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prototype)


def payload(action="dispatch_mobile_charger"):
    return {"action": action, "reason": "Pin dưới ngưỡng.",
            "message": "Dừng xe ở nơi an toàn, chờ điều phối viên xác nhận hỗ trợ.",
            "requires_human_approval": True}


def output(data=None):
    return prototype.DRAFT_PREFIX + json.dumps(data if data is not None else payload())


@pytest.mark.parametrize("action", ["dispatch_mobile_charger", "draft_message", "request_human_review"])
def test_valid_proposed_actions(action):
    assert prototype.validate_response(output(payload(action)), action)["action"] == action


@pytest.mark.parametrize("text", [
    "", "Tôi đã gửi [DRAFT_ONLY] ", " " + output(),
    "```json\n" + output() + "\n```", output() + " sent!",
    prototype.DRAFT_PREFIX + "[]", prototype.DRAFT_PREFIX + "null",
    prototype.DRAFT_PREFIX + '{"action":"dispatch_mobile_charger","action":"draft_message"}',
    prototype.DRAFT_PREFIX + "cứu hộ dispatch_mobile_charger",
])
def test_reject_malformed_or_misleading_output(text):
    with pytest.raises(ValueError):
        prototype.validate_response(text, "dispatch_mobile_charger")


@pytest.mark.parametrize("changes", [
    {"action": "draft_message"}, {"action": "send_now"}, {"action": []},
    {"requires_human_approval": False}, {"requires_human_approval": "true"},
    {"requires_human_approval": 1}, {"message": " "}, {"reason": ""},
    {"message": None}, {"reason": 123}, {"send_now": True},
])
def test_reject_schema_or_policy_violation(changes):
    data = payload()
    data.update(changes)
    with pytest.raises(ValueError):
        prototype.validate_response(output(data), "dispatch_mobile_charger")


def test_reject_missing_field():
    data = payload()
    del data["message"]
    with pytest.raises(ValueError):
        prototype.validate_response(output(data), "dispatch_mobile_charger")


def test_project_dotenv_takes_precedence_without_mutating_environment(tmp_path, monkeypatch):
    monkeypatch.setattr(prototype, "PROJECT_ROOT", tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "environment-test-value")
    (tmp_path / ".env").write_text('GEMINI_API_KEY="local-test-value"\n', encoding="utf-8")
    assert prototype.get_api_key() == "local-test-value"
    import os
    assert os.environ["GEMINI_API_KEY"] == "environment-test-value"


@pytest.mark.parametrize("name", ["GEMINI_API_KEY", "GOOGLE_API_KEY"])
def test_environment_key_fallback(name, tmp_path, monkeypatch):
    monkeypatch.setattr(prototype, "PROJECT_ROOT", tmp_path)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setenv(name, "test-only")
    assert prototype.get_api_key() == "test-only"


def test_evaluate_uses_system_instruction_and_returns_raw_output(monkeypatch):
    from google import genai

    client_factory = MagicMock()
    client = client_factory.return_value.__enter__.return_value
    client.models.generate_content.return_value.text = "  raw response without tag  "
    monkeypatch.setattr(prototype, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(genai, "Client", client_factory)
    assert prototype.evaluate_prompt("synthetic input") == "  raw response without tag  "
    args = client.models.generate_content.call_args.kwargs
    assert args["model"] == prototype.GEMINI_MODEL
    assert args["contents"] == "synthetic input"
    assert args["config"].system_instruction == prototype.SYSTEM_PROMPT
    assert args["config"].temperature == 0.0
    assert client_factory.call_args.kwargs["http_options"].timeout == 20000
    client_factory.return_value.__exit__.assert_called_once()


def test_empty_model_output_is_error(monkeypatch):
    from google import genai

    factory = MagicMock()
    factory.return_value.__enter__.return_value.models.generate_content.return_value.text = ""
    monkeypatch.setattr(prototype, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(genai, "Client", factory)
    with pytest.raises(RuntimeError, match="empty"):
        prototype.evaluate_prompt("synthetic")


def test_missing_key_stops_before_network(monkeypatch, capsys):
    monkeypatch.setattr(prototype, "get_api_key", lambda: None)
    assert prototype.main([]) == 1
    assert "No live tests" in capsys.readouterr().err
    with pytest.raises(RuntimeError, match="Set GEMINI_API_KEY"):
        prototype.evaluate_prompt("synthetic")


@pytest.mark.parametrize("error_type", [RuntimeError, ValueError])
def test_api_error_is_not_replaced_with_fake_success_or_leaked(monkeypatch, error_type):
    def api_error(_):
        raise error_type("sensitive-test-value")
    monkeypatch.setattr(prototype, "evaluate_prompt", api_error)
    result = prototype.run_case(prototype.ADVERSARIAL_TESTS[0])
    assert result["passed"] is False
    assert "output" not in result
    assert "sensitive-test-value" not in result["error"]


def test_main_returns_failure_and_saves_raw_rejected_output(tmp_path, monkeypatch):
    monkeypatch.setattr(prototype, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(prototype, "evaluate_prompt", lambda _: "unsafe raw output")
    report = tmp_path / "results/report.json"
    assert prototype.main(["--report", str(report)]) == 1
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["passed"] == 0
    assert data["total"] == 6
    assert all(r["output"] == "unsafe raw output" for r in data["results"])


def test_all_expected_outputs_give_success_exit_status(monkeypatch):
    cases = prototype.ADVERSARIAL_TESTS + prototype.CONTROL_TESTS
    expected = {c["input"]: output(payload(c["expected_action"])) for c in cases}
    monkeypatch.setattr(prototype, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(prototype, "evaluate_prompt", expected.__getitem__)
    assert prototype.main([]) == 0
