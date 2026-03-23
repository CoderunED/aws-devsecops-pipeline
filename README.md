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
| Trufflehog | Secret scanning in git history | 43 chunks scanned | 0 verified secrets |
| Checkov | IaC misconfiguration scanning | 41 checks | 26 failed, 15 passed |

## Vulnerabilities Detected (Demo App)

### Code vulnerabilities (Semgrep)
- `subprocess-shell-true` — command injection via shell=True
- `insecure-hash-algorithm-md5` — weak hashing algorithm
- `hardcoded-password` — credentials hardcoded in source (3 instances)
- `sql-injection-format` — SQL query built with string formatting
- `os-system-injection` — os.system() command injection

### Infrastructure misconfigurations (Checkov)
- S3 bucket public access enabled — 4 findings
- S3 bucket missing encryption, versioning, logging — 6 findings
- Security group open to 0.0.0.0 on all ports including SSH and RDP — 5 findings
- RDS database publicly accessible, unencrypted, no deletion protection — 11 findings

## Tech Stack
- GitHub Actions — CI/CD pipeline
- Semgrep — static analysis (SAST)
- Trufflehog — git history secret scanning
- Checkov — Terraform IaC misconfiguration scanning
- Python — scripting and custom rule logic
- AWS — target infrastructure
- Claude API — AI-powered security analysis (live)

## Current Status
- [x] GitHub Actions pipeline running
- [x] Semgrep SAST scanning (community + custom rules)
- [x] Trufflehog secret scanning
- [x] Checkov IaC scanning
- [x] Claude AI security summarizer
- [x] AI-powered PR comments
- [ ] Merge blocking on critical findings

## Metrics So Far
- 7 code vulnerabilities detected across 1 file
- 26 infrastructure misconfigurations caught before deployment
- 586 total Semgrep rules running on every push
- 43 git chunks scanned for leaked secrets
- Resources protected: S3, RDS, Security Groups, IAM
- Full scan completes in under 60 seconds

## What's Next
Posting AI summary automatically as pull request comments,
then adding merge blocking on critical findings.
