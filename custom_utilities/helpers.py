import base64
from datetime import timedelta, datetime
import time

def get_base64_image(path):
    if path:
        with open(path, 'rb') as image_obj:
            return base64.b64encode(image_obj.read()).decode("ascii")