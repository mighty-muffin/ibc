---
hide:
  - toc
---

# Dependabot

**Dependabot** is a built-in GitHub tool that automates the management of project
dependencies, scanning for outdated or vulnerable libraries and automatically
creating pull requests (PRs) to update them.

## Ecosystems

| Ecosystem        | Schedule       | Cooldown | Registry   |
| ---------------- | -------------- | -------- | ---------- |
| `docker`         | Monthly        | 7 days   | Docker Hub |
| `github-actions` | Daily          | 7 days   | GitHub     |
| `pre-commit`     | Weekly         | 7 days   | GitHub     |
| `pip` (Python)   | Daily (Sunday) | 7 days   | PyPI       |

> **Note:** The `pip` ecosystem is used instead of `uv` due to a known Dependabot
> bug where the `uv` file parser calls `pyenv exec pip install cython` to resolve
> Cython-based package metadata (triggered by `pycryptodome`) using a pip instance
> that does not trust Dependabot's internal proxy CA, causing SSL verification
> failures on every run. Switch back to `uv` once the upstream bug is fixed.

## Update Grouping

All ecosystems follow the same two-group strategy to limit PR noise and separate
low-risk from high-risk updates:

| Group          | Update types       | Review required |
| -------------- | ------------------ | --------------- |
| `*-minor-patch`| `minor`, `patch`   | No              |
| `*-major`      | `major`            | Yes             |

Minor and patch updates are batched into a single PR per ecosystem.
Major updates are isolated in their own PR to allow careful review before merging.

## Registries

Private registry URLs can be changed in the top-level `registries` block of
`.github/dependabot.yml`. Credentials are read from repository secrets:

| Registry key      | Secret vars                              |
| ----------------- | ---------------------------------------- |
| `docker-registry` | `DOCKER_USERNAME`, `DOCKER_PASSWORD`     |
| `pypi-registry`   | `PYPI_USERNAME`, `PYPI_PASSWORD`         |
