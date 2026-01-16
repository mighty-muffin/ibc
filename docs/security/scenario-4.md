---
hide:
  - toc
---

# Scenario 4

**Code Vulnerabilities (10–15 min):**

This project includes several code vulnerabilities in this codebase. Let’s focus on the [`src/web/views.py`](https://github.com/mighty-muffin/ibc/tree/main/src/web/views.py) file. The `get_file_checksum` function uses weak cryptography.

```python
def get_file_checksum(data: bytes) -> str:
    (dk, iv) = (secretKey, secretKey)
    crypter = DES.new(dk, DES.MODE_CBC, iv)
    padded = pad(data, DES.block_size)
    encrypted = crypter.encrypt(padded)
    return base64.b64encode(encrypted).decode("UTF-8")
```

The [Data Encryption Standard (DES)](https://en.wikipedia.org/wiki/Data_Encryption_Standard) was officially withdrawn from the NIST recommendations (May 19, 2005) because it no longer provided adequate security (vulnerable to brute-force attacks). This is an obvious example of [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html), which is a typical issue popularized with the [OWASP Top Ten 2025 Category A04:2025 - Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/). It has been replaced by stronger algorithms like the Advanced Encryption Standard (AES).

## Implementation

- Demonstrate how your platform can scan and find code vulnerabilities in this codebase.
- Demonstrate how your platform provides guidance toward resolution.
- Demonstrate how your platform implements or suggests vulnerability resolution (e.g., ease of use).
- Demonstrate how your platform focuses scanning only on new code.

```yaml
# insecure-bank/.github/workflows/branch.yml

  - name: Run SAST Scan
    id: sast
    run: |
      echo Run SAST Scan
      echo "::warning::Must implement a code scanning mechanism."
    shell: bash
```

- If your platform allows local scanning on a developer workstation **prior to pushing code** to the remote repository, please demonstrate how this is achieved.
- If your platform allows a "pipeless" scanning mechanism, please demonstrate how this is achieved.
- If your platform uses the CI pipeline as a scanning mechanism, make the required change in the [`branch.yml`](../pipeline/branches.md)  workflow, keeping the **id: sast** for tracking purposes.

> **_NOTE:_** Use the branch `demo/sast` to track changes in your fork.

## What to present

Present how, once your platform is implemented, the Application Security and Developers teams can find and understand SAST vulnerabilities.

For example, showcase your findings for this project, how they are prioritized, and why such priorities are suggested. Explain the overall vision for how code vulnerabilities are handled within your platform.

If your platform offers coding agent capabilities, showcase how it can be used to resolve the weak cryptography in the `get_file_checksum` function.

## Write Up[^1]

<!-- You can write your note and details here. -->

[^1]: You can merge changes made in `demo/waivers` into `demo/sast` as a starting point to carry over the storyline you are building.
