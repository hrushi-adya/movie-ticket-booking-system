import collections
from datetime import datetime, timezone
from decimal import Decimal


def generate_utc_timestamp():
    return datetime.now().isoformat()


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def decimal_to_native(obj):
    """Helper function to convert Decimal to int/float for JSON serialization."""
    if isinstance(obj, Decimal):
        # Convert to int if the Decimal represents a whole number, otherwise float
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    return obj