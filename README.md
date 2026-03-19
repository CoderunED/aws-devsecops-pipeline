# AWS DevSecOps Security Pipeline

An AI-powered DevSecOps pipeline that automatically scans code for security 
vulnerabilities on every push using GitHub Actions.

## The Problem
Security issues caught in production cost 10x more to fix than issues caught 
during development. Most teams don't have automated security gates in their 
CI/CD pipelines.

## The Solution
This pipeline automatically runs security scans on every code push and pull 
request — catching vulnerabilities before they ever reach production.

## Pipeline Overview
```
Code Push → SAST Scan → Secret Scan → IaC Scan → AI Summary → Gate
```

## Security Tools

| Tool | Purpose | Rules Run | Findings (demo) |
|------|---------|-----------|-----------------|
| Semgrep (community) | SAST — code vulnerabilities | 583 rules | 2 findings |
| Semgrep (custom) | Custom security rules | 3 custom rules | 5 findings |
| Trufflehog | Secret scanning in git history | — | coming soon |
| Checkov | IaC misconfiguration scanning | — | coming soon |

## Vulnerabilities Detected (Demo App)
- `subprocess-shell-true` — command injection via shell=True
- `insecure-hash-algorithm-md5` — weak hashing algorithm
- `hardcoded-password` — credentials hardcoded in source (3 instances)
- `sql-injection-format` — SQL query built with string formatting
- `os-system-injection` — os.system() command injection

## Tech Stack
- GitHub Actions — CI/CD pipeline
- Semgrep — static analysis (SAST)
- Python — scripting and custom rule logic
- AWS — target infrastructure (expanding)
- Claude API — AI-powered findings summary (coming Week 3)

- [x] GitHub Actions pipeline running
- [x] Semgrep SAST scanning (community + custom rules)
- [x] Trufflehog secret scanning
- [ ] Checkov IaC scanning
- [ ] AI-powered PR comments
- [ ] Merge blocking on critical findings
Push → Semgrep (7 findings) → Trufflehog (git history scan) → Results saved
## Metrics So Far
- 7 vulnerabilities detected across 1 file
- 586 total rules running on every push
- 2 blocking findings that would prevent a bad merge
- Scan completes in under 60 seconds

## What's Next
Adding Trufflehog for git history secret scanning, then Checkov for 
Terraform infrastructure scanning, then Claude AI to explain every 
finding in plain English directly on pull requests.
