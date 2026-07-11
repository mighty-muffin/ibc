# Issues

## Harden user-supplied file handling in avatar and image endpoints

File access is currently based on user-controlled path fragments with minimal validation, which makes the storage and download code easy to misuse.

Examples:
- `src/web/services.py:17-32` (`StorageService.exists/load/save`) joins `file_name` directly onto the avatar directory
- `src/web/views.py:167-183` (`AvatarView`, `AvatarUpdateView`) trusts `image` and writes files using the logged-in username without validating extension or content type
- `src/web/views.py:233-246` (`CreditCardImageView`) opens a file derived from the `url` query parameter without a whitelist or safe path normalization

Please normalize and validate filenames before use, constrain reads/writes to the expected directory, and reject unexpected extensions or missing parameters. Add tests for traversal-style inputs and invalid filenames.

## Remove pickle-based certificate flow and shell execution hooks

The certificate upload/download flow currently depends on unsafe serialization and command execution primitives.

Problem areas:
- `src/web/views.py:36-60` defines `Untrusted.__reduce__()` to call `os.system("ls -lah")` and `to_traces()` shells out via `os.system`
- `src/web/views.py:186-230` serializes certificates with `pickle.dumps()` and later accepts uploaded pickles through `pickle.loads()` after a checksum match

This pattern is unsafe by design and should be replaced with a non-executable format such as JSON or signed bytes via Django signing / HMAC. Please remove the shell-out helpers and make the certificate workflow reject any untrusted payloads without ever unpickling them.

## Replace raw SQL string concatenation in services

Several service helpers build SQL by concatenating untrusted input directly into query strings, which makes the data layer brittle and injection-prone.

Examples:
- `src/web/services.py:41-67` (`find_users_by_username_and_password`, `find_users_by_username`)
- `src/web/services.py:77-95` (`find_cash_accounts_by_username`, `get_from_account_actual_amount`, `get_id_from_number`)
- `src/web/services.py:100-115` (`find_credit_accounts_by_username`, `update_credit_account`)
- `src/web/services.py:119-127` (`find_transactions_by_cash_account_number`)

Please replace these with parameterized queries or ORM filters, then add regression tests covering usernames/account numbers with quotes and other special characters.

