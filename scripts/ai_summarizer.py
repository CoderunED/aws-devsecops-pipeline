import anthropic
import json
import os
import sys


def load_findings():
    all_findings = []

    for fname in ["semgrep-community.json", "semgrep-custom.json"]:
        if not os.path.exists(fname):
            print(f"Warning: {fname} not found, skipping")
            continue
        with open(fname) as f:
            data = json.load(f)
        findings = data.get("results", [])
        for finding in findings:
            all_findings.append({
                "rule": finding["check_id"].split(".")[-1],
                "file": finding["path"],
                "line": finding["start"]["line"],
                "severity": finding["extra"]["severity"],
                "message": finding["extra"]["message"]
            })

    return all_findings


def build_prompt(findings):
    if not findings:
        return None

    findings_text = ""
    for i, f in enumerate(findings, 1):
        findings_text += f"""
Finding {i}:
  Rule: {f['rule']}
  File: {f['file']} (line {f['line']})
  Severity: {f['severity']}
  Message: {f['message']}
"""

    prompt = f"""You are a senior security engineer reviewing automated scan results.
Below are security findings from a code scan. For each finding:
1. Explain what the vulnerability is in plain English (1-2 sentences)
2. Explain the real-world risk if exploited (1 sentence)
3. Give a specific code fix (show before and after)

Keep your tone clear and direct. This will be posted as a pull request comment.

FINDINGS:
{findings_text}

Format your response as:
## Security Scan Results — [X] findings

For each finding use this format:
### Finding [N]: [rule name]
**What it is:** ...
**Risk:** ...
**Fix:**
```python
# Before (vulnerable)
...
# After (secure)
...
```
"""
    return prompt


def call_claude(prompt):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def main():
    print("Loading security findings...")
    findings = load_findings()

    if not findings:
        print("No findings to summarize.")
        with open("ai-summary.md", "w") as f:
            f.write("## Security Scan Results\n\nNo findings detected. ✅")
        return

    print(f"Found {len(findings)} findings. Sending to Claude...")
    prompt = build_prompt(findings)
    summary = call_claude(prompt)

    with open("ai-summary.md", "w") as f:
        f.write(summary)

    print("=== AI SUMMARY ===")
    print(summary)
    print(f"\nSummary saved to ai-summary.md")


if __name__ == "__main__":
    main()
