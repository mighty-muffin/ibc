---
hide:
  - toc
---

# Scenario 5

**Container Vulnerabilities (10–15 min):**

This project is a containerized application based on Python 3.10 (Alpine) intended to be deployed via orchestration.

This project uses the upstream base image [python:3.10.11-alpine3.18](https://hub.docker.com/layers/library/python/3.10.11-alpine3.18/images/sha256-afc3587de3a1fed7d55822cedd07238c1803f21fdca609a0352282656a2c144a)[^2], which is aging and has not been updated in ages.

> **_NOTE:_** This project must remain on `python3.10.X-alpine-3.XX`; do not perform a MAJOR upgrade of Python or Alpine.

## Implementation

- Demonstrate how your platform can scan and find vulnerabilities in the upstream container.
- Demonstrate how your platform can scan and find vulnerabilities in the resulting container.
- Demonstrate how your platform can scan and find vulnerabilities in the [`Dockerfile`](https://github.com/mighty-muffin/ibc/tree/main/Dockerfile)
- Demonstrate how your platform provide guidance toward resolution.
- Demonstrate how your platform implement|suggest vulnerabilities resolution (i.e.: ease of use).

```yaml
# insecure-bank/.github/workflows/branch.yml

  - name: Run Container Scan
    id: container
    run: |
      echo Run Container Scan
      echo "::warning::Must implement a container scanning mechanism."
    shell: bash
```

- If your platform allows local scanning on a developer workstation **prior to pushing code** to the remote repository, please demonstrate how this is achieved.
- If your platform allows a "pipeless" scanning mechanism, please demonstrate how this is achieved.
- If your platform uses the CI pipeline as a scanning mechanism, make the required change in the [`branch.yml`](../pipeline/branches.md)  workflow, keeping the **id: container** for tracking purposes.

> **_NOTE:_** Use the branch `demo/container` to track changes in your fork.

## What to present

Present how, once your platform is implemented, the Application Security and Developers teams can find and understand container vulnerabilities.

For example, showcase your findings for this project, how they are prioritized, and why such priorities are suggested. Explain the overall vision for how container vulnerabilities are handled within your platform.

## Write Up[^1]

<!-- You can write your note and details here. -->

[^1]: You can merge changes made in `demo/sast` into `demo/container` as a starting point to carry over the storyline you are building.
[^2]: sha256:def82962a6ee048e54b5bec2fcdfd4aada4a907277ba6b0300f18c836d27f095
