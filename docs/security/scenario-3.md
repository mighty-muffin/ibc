---
hide:
  - toc
---

# Scenario 3

**Exemptions & Waivers (10–15 min):**

This project includes several other dependency vulnerabilities in this codebase.

> **_NOTE:_** Use the branch `demo/waivers` to track changes in your fork.

## Implementation

Demonstrate how your platform can generate exemptions and/or waivers to ignore all other dependency vulnerabilities until Feb 27, 2026.

```yaml
# insecure-bank/.github/workflows/branch.yml

  - name: Run SCA Scan
    id: sca
    run: |
      echo Run SCA Scan
      echo "::warning::Must implement a dependencies scanning mechanism."
    shell: bash
```

- If your platform allows local scanning on a developer workstation **prior to pushing code** to the remote repository, please demonstrate how the exemptions/waivers mechanism is handled.
- If your platform leverages the CI pipeline for the exemptions/waivers mechanism, make the required change in the [`branch.yml`](../pipeline/branches.md)  workflow, keeping the **id: sca** for tracking purposes.

> **_NOTE:_** Use the branch `demo/waivers` to track changes in your fork.

## What to present

Present how, once your platform is implemented, the Application Security and Developers teams can find and understand which dependency vulnerabilities are silenced, why, and until when. Explain the overall vision for how dependency vulnerability exemptions/waivers are handled within your platform.

## Write Up[^1]

<!-- You can write your note and details here. -->

[^1]: You can merge changes made in `demo/sca` into `demo/waivers` as a starting point to carry over the storyline you are building.
