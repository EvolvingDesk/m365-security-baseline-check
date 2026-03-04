#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

def build_report(tenant_name: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()

    checks = [
        {"id": "mfa_coverage", "status": "UNKNOWN", "note": "Template placeholder"},
        {"id": "admin_accounts", "status": "UNKNOWN", "note": "Template placeholder"},
        {"id": "mailbox_forwarding", "status": "UNKNOWN", "note": "Template placeholder"},
        {"id": "external_sharing", "status": "UNKNOWN", "note": "Template placeholder"},
        {"id": "audit_logging", "status": "UNKNOWN", "note": "Template placeholder"},
    ]

    summary = {
        "ok": 0,
        "warning": 0,
        "critical": 0,
        "unknown": len(checks),
    }

    return {
        "tool": "m365-security-baseline-template",
        "generated_at_utc": now,
        "tenant": tenant_name,
        "checks": checks,
        "summary": summary,
        "exit_code": 0,
        "status_note": "Starter template, not production ready",
    }

def write_output(report: dict, fmt: str, out_path: str | None) -> None:
    payload: str
    if fmt == "json":
        payload = json.dumps(report, indent=2, sort_keys=True)
    else:
        lines = []
        lines.append(f"Tool: {report['tool']}")
        lines.append(f"Generated: {report['generated_at_utc']}")
        lines.append(f"Tenant: {report['tenant']}")
        lines.append("")
        lines.append("Checks:")
        for c in report["checks"]:
            lines.append(f"  {c['id']}: {c['status']} , {c['note']}")
        lines.append("")
        s = report["summary"]
        lines.append(f"Summary: ok {s['ok']} , warning {s['warning']} , critical {s['critical']} , unknown {s['unknown']}")
        lines.append(f"Exit code: {report['exit_code']}")
        payload = "\n".join(lines)

    if out_path:
        Path(out_path).write_text(payload, encoding="utf-8")
    else:
        print(payload)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Starter template for a Microsoft 365 security baseline check. Not production ready."
    )
    parser.add_argument("--tenant", default="unknown", help="Tenant name label for the report")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--out", default=None, help="Write output to a file path instead of stdout")
    args = parser.parse_args()

    report = build_report(args.tenant)
    write_output(report, args.format, args.out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
