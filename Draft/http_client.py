import requests

class HttpClient:
    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"
    MULTIPART = "multipart/form-data"
    TEXT = "text/plain"
    HTML = "text/html"
    OCTET_STREAM = "application/octet-stream"

    def __init__(self, base_url=None, headers=None, timeout=30):
        self.base_url = base_url.rstrip('/') if base_url else ''
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, path='', params=None):
        url = self._build_url(path)
        try:
            response = self.session.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def post(self, path='', params=None, data=None, json=None, files=None):
        url = self._build_url(path)
        try:
            response = self.session.post(
                url, headers=self.headers, params=params,
                data=data, json=json, files=files, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"POST request failed: {e}")
            return None

    def _build_url(self, path):
        if path.startswith('http'):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"