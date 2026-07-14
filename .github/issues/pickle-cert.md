# Remove pickle-based certificate flow and shell execution hooks

The certificate upload/download flow currently depends on unsafe serialization and command execution primitives.

Problem areas:
- `src/web/views.py:36-60` defines `Untrusted.__reduce__()` to call `os.system("ls -lah")` and `to_traces()` shells out via `os.system`
- `src/web/views.py:186-230` serializes certificates with `pickle.dumps()` and later accepts uploaded pickles through `pickle.loads()` after a checksum match

This pattern is unsafe by design and should be replaced with a non-executable format such as JSON or signed bytes via Django signing / HMAC. Please remove the shell-out helpers and make the certificate workflow reject any untrusted payloads without ever unpickling them.
