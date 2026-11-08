from datetime import datetime

def parse_date(date_str):
    """Parse MM/DD/YY or ISO date strings."""
    try:
        return datetime.strptime(date_str, "%m/%d/%y")
    except ValueError:
        return datetime.fromisoformat(date_str)
