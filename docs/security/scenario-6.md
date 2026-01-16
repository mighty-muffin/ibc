---
hide:
  - toc
---

# Scenario 6

**SBOM Generation (10–15 min):**

This project is a key application, and a software bill of materials (SBOM) is required for compliance purposes.

Regardless of exemptions and waivers, the SBOM must be an immutable artifact attesting to the contents of this web application.

## Implementation

- Demonstrate how your platform can generate an immutable SBOM.
- Demonstrate how your platform can generate a SBOM for the final container binary.
- Demonstrate how your platform can scan and find vulnerabilities from a SBOM.
- Demonstrate how your platform provide guidance toward resolution.

```yaml
# insecure-bank/.github/workflows/branch.yml

  - name: Run Container Scan
    id: container
    run: |
      echo Run Container Scan
      echo "::warning::Must implement a container scanning mechanism."
    shell: bash
```

- If your platform allows local SBOM generation on a developer workstation, please demonstrate how this is achieved.
- If your platform allows a "pipeless" SBOM generation mechanism, please demonstrate how this is achieved.
- If your platform uses the CI pipeline for SBOM generation, make the required change in the [`branch.yml`](../pipeline/branches.md)  for tracking purposes.

> **_NOTE:_** Use the branch `demo/sbom` to track changes in your fork.

## What to present

Present how, once your platform is implemented, the Application Security and Developers teams can find and understand SBOM content and vulnerabilities.

For example, showcase your findings for this project, how they are prioritized, and why such priorities are suggested. Explain the overall vision for how SBOMs are handled within your platform.

## Write Up[^1]

<!-- You can write your note and details here. -->

[^1]: You can merge changes made in `demo/container` into `demo/sbom` as a starting point to carry over the storyline you are building.
