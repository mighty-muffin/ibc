# Replace raw SQL string concatenation in services

Several service helpers build SQL by concatenating untrusted input directly into query strings, which makes the data layer brittle and injection-prone.

Examples:
- `src/web/services.py:41-67` (`find_users_by_username_and_password`, `find_users_by_username`)
- `src/web/services.py:77-95` (`find_cash_accounts_by_username`, `get_from_account_actual_amount`, `get_id_from_number`)
- `src/web/services.py:100-115` (`find_credit_accounts_by_username`, `update_credit_account`)
- `src/web/services.py:119-127` (`find_transactions_by_cash_account_number`)

Please replace these with parameterized queries or ORM filters, then add regression tests covering usernames/account numbers with quotes and other special characters.
