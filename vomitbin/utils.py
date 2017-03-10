import base64
import hashlib
import datetime

def new_paste_id(value):
    date = datetime.datetime.utcnow().isoformat()
    return base64.urlsafe_b64encode(hashlib.sha1('{}{}'.format(date, value).encode('utf-8')).digest()).decode('utf-8')
