---
hide:
  - toc
---
# Security Overview

The project is for educational purposes. These are the instructions for the upcoming demonstration. It requires about 6–8 hours of work to integrate, run, and accomplish these steps with our current tooling.

## Setup

- [ ] Fork the [insecure-bank-corp](https://github.com/mighty-muffin/ibc) with all branches
- [ ] Read the project documentation
- [ ] Verify everything works
- [ ] Run `make all` from the `Makefile`

## Scenario

Please take a look at each of the following six (6) scenario.

1. [SDLC Bad Practices](scenario-1.md)
2. [Dependency Vulnerabilities](scenario-2.md)
3. [Exemption & Waivers](scenario-3.md)
4. [Code Vulnerabilities](scenario-4.md)
5. [Container Vulnerabilities](scenario-5.md)
6. [SBOM Generation](scenario-6.md)

If required use the [Branches Pipeline](../pipeline/branches.md) to implement any workflow steps.

## And everything in between

- Showcases whatever you wish to highlight during the demonstration
- Highlights **shift-left**[^1] capabilities has much as possible recommended
- Allocates the available time to scenario you can present; if you cannot demonstrate a scenario
- Ignores all **hardcoded** or **leaked credentials**; [GitGuardian](https://github.com/GitGuardian/ggshield) will take care of them

[^1]: [Shift-left testing](https://en.wikipedia.org/wiki/Shift-left_testing)
