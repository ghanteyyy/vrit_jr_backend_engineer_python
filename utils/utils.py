import string
import secrets


def generate_uuid_hex():
    '''
    Generates a unique value
    '''

    return secrets.token_hex(32)


def generate_short_key():
    '''
    Generates a unique 7-characters short url value
    '''

    base = string.ascii_letters + string.digits

    return ''.join([secrets.choice(base) for _ in range(7)])
