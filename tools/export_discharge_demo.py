"""Nhóm A95 - export a validated SYNTHETIC draft, never a signed clinical note.
Chu Quang Linh <Quanglinh1286@gmail.com>; Nguyễn Minh Quân <minhquandhtb@gmail.com>;
Trương Thu Hà <thuha261102@gmail.com>; Phan Trần Mạnh Cường <manhcuong2005.28@gmail.com>;
Nguyễn Lương Phúc <luongphuc.lpu@gmail.com>.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discharge", ROOT / "starter-code/prompt_prototype.py")
prototype = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prototype)


def main():
    report = json.loads((ROOT / "results/gemini-discharge.json").read_text(encoding="utf-8"))
    if (report["use_case"] != "synthetic_discharge_summary"
            or report["system_prompt_sha256"] != hashlib.sha256(prototype.SYSTEM_PROMPT.encode()).hexdigest()):
        raise ValueError("Report does not match the current discharge-summary prototype.")
    case = prototype.CONTROL_TESTS[0]
    result = next(r for r in report["results"]
                  if r["name"] == case["name"] and r["input"] == case["input"])
    data = prototype.validate_response(result["output"], case["record"])
    headings = {
        "admission": "Thông tin nhập / xuất viện", "diagnoses": "Chẩn đoán theo hồ sơ",
        "hospital_course": "Diễn biến điều trị", "discharge_medications": "Thuốc theo nguồn giả lập",
        "allergies": "Dị ứng theo hồ sơ", "follow_up": "Kế hoạch theo dõi đã ghi",
        "pending_tests": "Xét nghiệm đang chờ", "discharge_condition": "Tình trạng xuất viện theo ghi chép",
    }
    lines = [
        "# [DRAFT_ONLY] Nhóm A95 - Tóm tắt hồ sơ xuất viện GIẢ LẬP",
        "",
        "Chu Quang Linh <Quanglinh1286@gmail.com>; Nguyễn Minh Quân <minhquandhtb@gmail.com>;",
        "Trương Thu Hà <thuha261102@gmail.com>; Phan Trần Mạnh Cường <manhcuong2005.28@gmail.com>;",
        "Nguyễn Lương Phúc <luongphuc.lpu@gmail.com>.",
        "",
        "> CHƯA ĐƯỢC BÁC SĨ PHÊ DUYỆT. Hồ sơ, bệnh và thuốc DEMO hoàn toàn giả lập;",
        "> không sử dụng cho người bệnh thật, không phải đơn thuốc hoặc quyết định xuất viện.",
        "",
        f"**Mã giả lập:** {data['patient_id']}",
        "",
        "**Trạng thái:** Bản nháp cần bác sĩ đối chiếu và phê duyệt.",
    ]
    for section in prototype.SECTIONS:
        lines.extend(["", "## " + headings[section], ""])
        lines.extend(f"- {entry['quote']} (Nguồn: {entry['source_id']})"
                     for entry in data["sections"][section])
    lines.extend(["", "Nguồn đối chiếu: fixture tổng hợp trong prototype; "
                  "[raw Gemini report](../results/gemini-discharge.json).", ""])
    output = ROOT / "output/discharge-summary-demo.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print("Exported validated synthetic demo: output/discharge-summary-demo.md")


if __name__ == "__main__":
    main()
