---
name: security-remediation
description: How to remediate an already-identified security finding in code, and what a security pull request must document.
---

# Security Remediation

Use this skill on the `security` path. A security issue describes an **already-identified** finding (from SAST/DAST, a scanner, or a human report). Your job is **in-code remediation** — fix the root cause in the application code and prove it with tests.

## Scope

- **In scope:** changing application/config/code so the weakness no longer exists.
- **Out of scope:** dependency / SCA **version bumps**. Those are owned by Dependabot. If a finding can *only* be resolved by upgrading a dependency, do **not** edit lockfiles or manifests to bump a version — instead note this in the PR/comment and defer to Dependabot.

## How to remediate

1. **Confirm the root cause** in code — the exact sink and the untrusted input that reaches it.
2. **Apply the standard fix pattern** for the weakness class. Common web-app patterns:

   | Weakness (CWE) | Fix pattern |
   |---|---|
   | SQL Injection (CWE-89) | Parameterised queries / ORM bindings; never string-format SQL. |
   | XSS (CWE-79) | Contextual output encoding; keep template auto-escaping on; sanitise HTML. |
   | CSRF (CWE-352) | Enforce anti-CSRF tokens / `SameSite` cookies on state-changing routes. |
   | IDOR / broken access control (CWE-639/285) | Authorise every object access against the caller. |
   | Path Traversal (CWE-22) | Canonicalise and confine paths to an allow-listed base directory. |
   | Command Injection (CWE-78) | Avoid the shell; pass argument vectors; allow-list inputs. |
   | SSRF (CWE-918) | Allow-list destinations; block internal/link-local ranges. |
   | XXE (CWE-611) | Disable external entities / DTDs in the XML parser. |
   | Insecure Deserialization (CWE-502) | Use safe formats; never deserialise untrusted data. |
   | Weak Crypto (CWE-327/326) | Use vetted, current algorithms and key lengths. |

3. **Update the tests.** If a test asserted the *vulnerable* behaviour, change it to assert the *fixed* behaviour (e.g. that an injection payload is now rejected). Keep the suite and any coverage gate green.

## What the security PR must document

In addition to the standard `resolve-issue-pr` quality bar, include:

- the **CWE** (and **CVE**, if any) identifier(s);
- a **severity** rating (critical / high / medium / low) justified by impact and exploitability;
- the **root cause** and how the flaw could be exploited;
- the **exact remediation** applied, referencing the changed lines.

## A touch of whimsy

In the security PR body, include exactly one short riddle, joke, or fun fact about **goblins or gnomes** as a trailing aside, clearly set apart from the remediation detail. Keep it brief; never mix it into the CWE/severity/root-cause content, the fix itself, or any test assertion. Never skip it.
