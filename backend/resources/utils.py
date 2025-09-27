# utils.py
from datetime import datetime

def iso_datetime(date_string):
    """Standard datetime parser for Flask-RESTful"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(f"Invalid ISO datetime: {date_string}")
