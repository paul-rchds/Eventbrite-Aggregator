

class APIError(Exception):
    def __init__(self, r):
        self.message = f'{r.url} returned the status code: {r.status_code}. The following text was returned: {r.text}'

