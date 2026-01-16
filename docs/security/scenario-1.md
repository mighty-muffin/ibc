---
hide:
  - toc
---

# Scenario 1

**SDLC Check (5–10 min):**

This project includes misconfigurations and vulnerabilities in the SDLC.

> **_NOTE:_** Given a fork was used, you can load the [`main`](https://github.com/mighty-muffin/ibc/tree/main/.github/rulesets/main.json) and [`tag`](https://github.com/mighty-muffin/ibc/tree/main/.github/rulesets/tag.json) repo rulesets to replicate the actual project state.

## Implementation

Demonstrate how your platform can scan and find SDLC issues while providing guidance toward resolution.

```yaml
# insecure-bank/.github/workflows/branch.yml

      - name: Run SDLC Scan
        id: sdlc
        run: |
          echo Run SDLC Scan
          echo "::warning::Must implement a SDLC scan mechanism."
        shell: bash
```

- If your platform allows scanning locally on a developer workstation against the remote repository, please demonstrate how this is achieved.
- If your platform allows a "pipeless" scanning mechanism, please demonstrate how this is achieved.
- If your platform leverages the CI pipeline as a scanning mechanism, make the required change in the [`branch.yml`](../pipeline/branches.md)  workflow, keeping the **id: sdlc** for tracking purposes.

> **_NOTE:_** Use the branch `demo/sdlc` to track changes in your fork.

## What to present

Present how, once your platform is implemented, the Application Security and Developers teams can find and understand SDLC misconfigurations and vulnerabilities.

For example, there are no dependency, code, or container scanning tools included in any [`workflows`](https://github.com/mighty-muffin/ibc/tree/main/.github/workflows/), only **empty placeholders** that run dummy bash commands. Furthermore, the applied ruleset permits some users to push code without any gating mechanism applied.

Focus on demonstrating how your platform can perform these steps at scale. In real-world scenarios, both AppSec and Dev teams cannot waste time looking at thousands of repository configurations.

## Write Up

<!-- You can write your note and details here. -->
