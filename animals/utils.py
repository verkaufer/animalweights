from datetime import datetime
from time import mktime


def transform_to_unixtime(timestamp: datetime) -> float:
    return mktime(timestamp.timetuple())
