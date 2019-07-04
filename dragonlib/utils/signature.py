import hashlib
import hmac

def generate(key, raw):
    s = hmac.new(bytes(key, encoding='utf8'), bytes(raw, encoding='utf8'), digestmod=hashlib.sha256).digest()
    return s.hex().lower()