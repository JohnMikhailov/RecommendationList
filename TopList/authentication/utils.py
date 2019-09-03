from datetime import datetime, timedelta

import jwt

from TopList import settings


def create_token(payload, token_type, ttl=None):
    if token_type == 'refresh':
        ttl_ = ttl or settings.JWT_REFRESH_TTL
    else:
        ttl_ = ttl or settings.JWT_ACCESS_TTL
    token = jwt.encode({'exp': datetime.utcnow() + timedelta(seconds=ttl_),
                        'type': token_type,
                        **payload}, settings.SECRET_KEY, algorithm='HS256').decode('UTF-8')
    return token
