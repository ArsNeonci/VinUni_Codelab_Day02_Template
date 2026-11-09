"""Nhóm A95 - discharge-summary regression tests; all patient data is fictional.
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
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


def draft(record=None, action="draft_discharge_summary", missing=None, issues=None):
    record = p.synthetic_record() if record is None else record
    sections = {section: [] for section in p.SECTIONS}
    for source in record["sources"]:
        if source["patient_id"] == record["patient_id"] and source["section"] in sections:
            sections[source["section"]].append({"source_id": source["id"], "quote": source["text"]})
    return {"action": action, "patient_id": record["patient_id"], "sections": sections,
            "missing_fields": missing or [], "issues": issues or [],
            "requires_clinician_approval": True}


def output(data=None):
    return p.DRAFT_PREFIX + json.dumps(draft() if data is None else data, ensure_ascii=False)


def test_complete_chart_keeps_dose_allergy_and_pending_results():
    data = p.validate_response(output(), p.synthetic_record())
    assert "10 mg" in data["sections"]["discharge_medications"][0]["quote"]
    assert "chất-DEMO-X" in data["sections"]["allergies"][0]["quote"]
    assert "đang chờ" in data["sections"]["pending_tests"][0]["quote"]
    assert data["requires_clinician_approval"] is True


@pytest.mark.parametrize("index,missing,issues", [
    (0, ["allergies", "diagnoses"], ["missing_data"]),
    (1, [], []), (2, [], []), (3, [], []),
    (4, ["allergies", "diagnoses"], ["missing_data", "mixed_patient_records"]),
    (5, [], ["conflicting_records"]), (6, [], []),
])
def test_adversarial_chart_policy_has_explicit_oracle(index, missing, issues):
    case = p.ADVERSARIAL_TESTS[index]
    data = draft(case["record"], case["expected_action"], missing, issues)
    checked = p.validate_response(output(data), case["record"])
    assert checked["action"] == case["expected_action"]


@pytest.mark.parametrize("text", [
    "", "Đã ký [DRAFT_ONLY] ", " " + output(),
    "```json\n" + output() + "\n```", output() + " approved",
    p.DRAFT_PREFIX + "[]", p.DRAFT_PREFIX + "null",
    p.DRAFT_PREFIX + '{"action":"draft_discharge_summary","action":"approved"}',
])
def test_reject_malformed_or_misplaced_draft_tag(text):
    with pytest.raises(ValueError):
        p.validate_response(text, p.synthetic_record())


@pytest.mark.parametrize("changes", [
    {"action": "approved"}, {"action": []}, {"patient_id": "SYNTH-002"},
    {"requires_clinician_approval": False}, {"requires_clinician_approval": "true"},
    {"requires_clinician_approval": 1}, {"signed": True}, {"sections": []},
    {"missing_fields": ["diagnoses"]}, {"issues": ["missing_data"]},
    {"issues": "none"},
])
def test_reject_invalid_schema_approval_or_claimed_readiness(changes):
    data = draft()
    data.update(changes)
    with pytest.raises(ValueError):
        p.validate_response(output(data), p.synthetic_record())


def test_reject_missing_approval_field():
    data = draft()
    del data["requires_clinician_approval"]
    with pytest.raises(ValueError):
        p.validate_response(output(data), p.synthetic_record())


@pytest.mark.parametrize("section,replacement", [
    ("discharge_medications", "Thuốc-DEMO-A 100 mg, tự tăng liều."),
    ("diagnoses", "Chẩn đoán mới không có trong bệnh án."),
    ("pending_tests", "Xét nghiệm-DEMO-D bình thường."),
    ("allergies", "Không có dị ứng."),
    ("follow_up", "Tái khám vào ngày khác."),
])
def test_reject_fabricated_or_modified_clinical_text(section, replacement):
    data = draft()
    data["sections"][section][0]["quote"] = replacement
    with pytest.raises(ValueError, match="source text"):
        p.validate_response(output(data), p.synthetic_record())


def test_reject_omitted_pending_test():
    data = draft()
    data["sections"]["pending_tests"] = []
    with pytest.raises(ValueError, match="omitted"):
        p.validate_response(output(data), p.synthetic_record())


def test_reject_foreign_patient_diagnosis_even_with_valid_source_id():
    case = p.ADVERSARIAL_TESTS[4]
    data = draft(case["record"], "request_clinician_review",
                 ["allergies", "diagnoses"], ["missing_data", "mixed_patient_records"])
    foreign = case["record"]["sources"][-1]
    data["sections"]["diagnoses"].append({"source_id": foreign["id"], "quote": foreign["text"]})
    with pytest.raises(ValueError, match="foreign"):
        p.validate_response(output(data), case["record"])


def test_reject_silently_resolved_medication_conflict():
    case = p.ADVERSARIAL_TESTS[5]
    data = draft(case["record"], "request_clinician_review", issues=["conflicting_records"])
    data["sections"]["discharge_medications"].pop()
    with pytest.raises(ValueError, match="omitted"):
        p.validate_response(output(data), case["record"])


def test_missing_chart_is_review_only_with_empty_sections():
    record = {"synthetic": True, "patient_id": "SYNTH-EMPTY", "sources": []}
    data = draft(record, "request_clinician_review", list(p.SECTIONS), ["missing_data"])
    assert p.validate_response(output(data), record)["action"] == "request_clinician_review"
    data["action"] = "draft_discharge_summary"
    with pytest.raises(ValueError, match="policy"):
        p.validate_response(output(data), record)


def test_reject_duplicate_source_and_wrong_section():
    data = draft()
    data["sections"]["diagnoses"].append(data["sections"]["admission"][0])
    with pytest.raises(ValueError, match="Duplicate source or wrong section"):
        p.validate_response(output(data), p.synthetic_record())


def test_reject_missing_section_and_duplicate_source_ids():
    data = draft()
    del data["sections"]["allergies"]
    with pytest.raises(ValueError, match="eight sections"):
        p.validate_response(output(data), p.synthetic_record())
    record = p.synthetic_record()
    record["sources"].append(record["sources"][0].copy())
    with pytest.raises(ValueError, match="identifiers"):
        p.validate_response(output(), record)


def test_project_dotenv_precedes_environment_without_mutating_it(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "PROJECT_ROOT", tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "environment-test-value")
    (tmp_path / ".env").write_text('GEMINI_API_KEY="local-test-value"\n', encoding="utf-8")
    assert p.get_api_key() == "local-test-value"
    import os
    assert os.environ["GEMINI_API_KEY"] == "environment-test-value"


@pytest.mark.parametrize("name", ["GEMINI_API_KEY", "GOOGLE_API_KEY"])
def test_environment_key_fallback(name, tmp_path, monkeypatch):
    monkeypatch.setattr(p, "PROJECT_ROOT", tmp_path)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setenv(name, "test-only")
    assert p.get_api_key() == "test-only"


def test_sdk_configuration_and_raw_output_not_repaired(monkeypatch):
    from google import genai
    factory = MagicMock()
    client = factory.return_value.__enter__.return_value
    client.models.generate_content.return_value.text = "  raw response  "
    monkeypatch.setattr(p, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(genai, "Client", factory)
    user_input = p.CONTROL_TESTS[0]["input"]
    assert p.evaluate_prompt(user_input) == "  raw response  "
    args = client.models.generate_content.call_args.kwargs
    assert args["model"] == "gemini-3.8-flash"
    assert args["contents"] == user_input
    assert args["config"].system_instruction == p.SYSTEM_PROMPT
    assert args["config"].thinking_config.thinking_level == "LOW"
    assert args["config"].temperature == 0.0
    assert factory.call_args.kwargs["http_options"].timeout == 20000
    factory.return_value.__exit__.assert_called_once()


def test_empty_model_response_is_error(monkeypatch):
    from google import genai
    factory = MagicMock()
    factory.return_value.__enter__.return_value.models.generate_content.return_value.text = ""
    monkeypatch.setattr(p, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(genai, "Client", factory)
    with pytest.raises(RuntimeError, match="empty"):
        p.evaluate_prompt(p.CONTROL_TESTS[0]["input"])


def test_missing_key_stops_before_network(monkeypatch, capsys):
    monkeypatch.setattr(p, "get_api_key", lambda: None)
    assert p.main([]) == 1
    assert "No live tests" in capsys.readouterr().err
    with pytest.raises(RuntimeError, match="Set GEMINI_API_KEY"):
        p.evaluate_prompt(p.CONTROL_TESTS[0]["input"])


@pytest.mark.parametrize("error_type", [RuntimeError, ValueError])
def test_api_failure_is_not_faked_or_leaked(error_type, monkeypatch):
    def fail(_):
        raise error_type("sensitive-test-value")
    monkeypatch.setattr(p, "evaluate_prompt", fail)
    result = p.run_case(p.CONTROL_TESTS[0])
    assert result["passed"] is False
    assert "output" not in result
    assert "sensitive-test-value" not in result["error"]


def test_failed_output_saved_raw_and_exit_nonzero(tmp_path, monkeypatch):
    monkeypatch.setattr(p, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(p, "evaluate_prompt", lambda _: "unsafe raw output")
    report = tmp_path / "results/report.json"
    assert p.main(["--report", str(report)]) == 1
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["passed"] == 0 and data["total"] == 8
    assert data["use_case"] == "synthetic_discharge_summary"
    assert all(r["output"] == "unsafe raw output" for r in data["results"])


def test_success_exit_with_mocked_grounded_outputs(monkeypatch):
    cases = p.ADVERSARIAL_TESTS + p.CONTROL_TESTS
    expected = {}
    for index, case in enumerate(cases):
        missing = ["allergies", "diagnoses"] if index in (0, 4) else []
        issues = {0: ["missing_data"], 4: ["missing_data", "mixed_patient_records"],
                  5: ["conflicting_records"]}.get(index, [])
        expected[case["input"]] = output(draft(case["record"], case["expected_action"], missing, issues))
    monkeypatch.setattr(p, "get_api_key", lambda: "test-only")
    monkeypatch.setattr(p, "evaluate_prompt", expected.__getitem__)
    assert p.main([]) == 0
