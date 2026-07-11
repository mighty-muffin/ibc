# Harden user-supplied file handling in avatar and image endpoints

File access is currently based on user-controlled path fragments with minimal validation, which makes the storage and download code easy to misuse.

Examples:
- `src/web/services.py:17-32` (`StorageService.exists/load/save`) joins `file_name` directly onto the avatar directory
- `src/web/views.py:167-183` (`AvatarView`, `AvatarUpdateView`) trusts `image` and writes files using the logged-in username without validating extension or content type
- `src/web/views.py:233-246` (`CreditCardImageView`) opens a file derived from the `url` query parameter without a whitelist or safe path normalization

Please normalize and validate filenames before use, constrain reads/writes to the expected directory, and reject unexpected extensions or missing parameters. Add tests for traversal-style inputs and invalid filenames.
