import json
from datetime import datetime, timedelta
import re
from dateutil import parser


def convert_linkedin_relative_datetime_to_date(timestamp):
    patterns = {
        r'(\d+)h': lambda x: datetime.now() - timedelta(hours=int(x.group(1))),   
        r'(\d+)d': lambda x: datetime.now() - timedelta(days=int(x.group(1))),    
        r'(\d+)m': lambda x: datetime.now() - timedelta(minutes=int(x.group(1))),
        r'(\d+)w': lambda x: datetime.now() - timedelta(weeks=int(x.group(1))),   
        r'(\d+)mo': lambda x: datetime.now() - timedelta(days=int(x.group(1)) * 30),
    }

    for pattern, func in patterns.items():
        match = re.match(pattern, timestamp)
        if match:
            return func(match).strftime('%Y-%m-%d')

    try:
        return parser.parse(timestamp).strftime('%Y-%m-%d')
    except ValueError:
        pass

    return None