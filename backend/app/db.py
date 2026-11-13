"""In‑memory database placeholder for the MVP.

The function ``get_database_value`` returns a static integer. In a real deployment
this would query a proper database (PostgreSQL, SQLite, etc.) but keeping the
logic trivial is sufficient for the skeleton and the smoke test.
"""

def get_database_value() -> int:
    """Return a sample value representing data stored in the database.

    Returns
    -------
    int
        A constant integer that the frontend will display.
    """
    return 42
