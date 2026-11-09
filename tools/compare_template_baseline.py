"""Nhóm A95 - compare a deterministic template with saved synthetic live output.
Chu Quang Linh <Quanglinh1286@gmail.com>; Nguyễn Minh Quân <minhquandhtb@gmail.com>;
Trương Thu Hà <thuha261102@gmail.com>; Phan Trần Mạnh Cường <manhcuong2005.28@gmail.com>;
Nguyễn Lương Phúc <luongphuc.lpu@gmail.com>.
No API calls, patient care, or claim of clinical effectiveness.
"""

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discharge", ROOT / "starter-code/prompt_prototype.py")
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


def template_draft(record):
    eligible, missing, issues = p.chart_policy(record)
    sections = {key: [] for key in p.SECTIONS}
    for source in eligible.values():
        sections[source["section"]].append({"source_id": source["id"], "quote": source["text"]})
    data = {
        "action": "request_clinician_review" if issues else "draft_discharge_summary",
        "patient_id": record["patient_id"], "sections": sections,
        "missing_fields": missing, "issues": issues, "requires_clinician_approval": True,
    }
    return p.DRAFT_PREFIX + json.dumps(data, ensure_ascii=False)


def main():
    saved = json.loads((ROOT / "results/gemini-discharge.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(p.SYSTEM_PROMPT.encode()).hexdigest()
    if saved["system_prompt_sha256"] != digest:
        raise ValueError("Saved live output uses another system prompt.")
    cases = p.ADVERSARIAL_TESTS + p.CONTROL_TESTS
    results = []
    for case in cases:
        original = next(r for r in saved["results"]
                        if r["name"] == case["name"] and r["input"] == case["input"])
        live_data = p.validate_response(original["output"], case["record"])
        template = template_draft(case["record"])
        template_data = p.validate_response(template, case["record"])
        if live_data["action"] != case["expected_action"] or template_data["action"] != case["expected_action"]:
            raise ValueError("Predeclared action mismatch.")
        results.append({
            "name": case["name"], "template_passed": True, "saved_live_passed": True,
            "same_action": live_data["action"] == template_data["action"],
            "template_output": template,
        })
    report = {
        "use_case": "synthetic_discharge_summary", "mode": "offline_template_comparison",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system_prompt_sha256": digest, "saved_live_model": saved["model"],
        "saved_live_report_sha256": hashlib.sha256((ROOT / "results/gemini-discharge.json").read_bytes()).hexdigest(),
        "api_calls_in_this_comparison": 0, "total": len(results),
        "template_passed": len(results), "saved_live_passed": len(results),
        "limitation": "Structured, pre-labelled fixtures; shared validator; no clinical or time-saving evaluation.",
        "results": results,
    }
    (ROOT / "results/template-baseline.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Template {len(results)}/{len(results)}; saved Gemini {len(results)}/{len(results)}; new API calls: 0.")
    print("No LLM advantage demonstrated on these pre-labelled fixtures.")


if __name__ == "__main__":
    main()
