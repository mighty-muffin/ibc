---
hide:
  - toc
---

# Scenario 2

**Dependency Vulnerabilities (10–15 min):**

This project includes dependency vulnerabilities in this codebase.

The version of [PyYAML@5.3.1](https://pypi.org/project/PyYAML/5.3.1/) included in this project’s `pyproject.toml` is vulnerable according to [CVE-2020-14343](https://nvd.nist.gov/vuln/detail/cve-2020-14343) and [CVE-2020-1747](https://nvd.nist.gov/vuln/detail/cve-2020-1747). The recommendation is to upgrade PyYAML to version 5.4 or higher.

Here the a [technical exploit writeup](https://hackmd.io/@harrier/uiuctf20) explaining the issue with this dependency.

## Implementation

Demonstrate how your platform can scan and find dependency vulnerabilities in this codebase.

```yaml
# insecure-bank/.github/workflows/branch.yml

  - name: Run SCA Scan
    id: sca
    run: |
      echo Run SCA Scan
      echo "::warning::Must implement a dependencies scanning mechanism."
    shell: bash
```

- If your platform allows local scanning on a developer workstation **prior to pushing code** to the remote repository, please demonstrate how this is achieved.
- If your platform allows a "pipeless" scanning mechanism, please demonstrate how this is achieved.
- If your platform uses the CI pipeline as a scanning mechanism, make the required change in the [`branch.yml`](../pipeline/branches.md)  workflow, keeping the **id: sca** for tracking purposes.

> **_NOTE:_** Use the branch `demo/sca` to track changes in your fork.

## What to present

Present how, once your platform is implemented, the Application Security and Developers teams can find and understand SCA vulnerabilities.

For example, showcase your findings for this project, how they are prioritized, and why such priorities are suggested. Explain the overall vision for how dependency vulnerabilities are handled within your platform.

## Write Up[^1]

<!-- You can write your note and details here. -->

[^1]: You can merge changes made in `demo/sdlc` into `demo/sca` as a starting point to carry over the storyline you are building.
