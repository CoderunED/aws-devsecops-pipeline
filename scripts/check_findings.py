import json
import sys
import os


def check_semgrep_findings():
    critical_findings = []
    all_findings = []

    for fname in ["semgrep-community.json", "semgrep-custom.json"]:
        if not os.path.exists(fname):
            continue
        with open(fname) as f:
            data = json.load(f)
        findings = data.get("results", [])
        for finding in findings:
            severity = finding["extra"]["severity"]
            rule = finding["check_id"].split(".")[-1]
            path = finding["path"]
            line = finding["start"]["line"]
            all_findings.append({
                "severity": severity,
                "rule": rule,
                "path": path,
                "line": line
            })
            if severity in ["ERROR", "CRITICAL"]:
                critical_findings.append({
                    "severity": severity,
                    "rule": rule,
                    "path": path,
                    "line": line
                })

    print(f"=== SECURITY GATE ===")
    print(f"Total findings: {len(all_findings)}")
    print(f"Critical/Error findings: {len(critical_findings)}")
    print()

    if critical_findings:
        print("🚨 BLOCKING — Critical findings detected:")
        for f in critical_findings:
            print(f"  [{f['severity']}] {f['path']}:{f['line']} — {f['rule']}")
        print()
        print("PR cannot be merged until these are resolved.")
        sys.exit(1)
    else:
        print("✅ PASSED — No critical findings. PR can be merged.")
        sys.exit(0)


if __name__ == "__main__":
    check_semgrep_findings()
