import requests


class AviationWeatherClient:
    BASE_URL = "https://www.aviationweather.gov/api/data/dataserver"

    def __init__(self, *args, **kwargs):
        pass

    def _get_headers(self):
        return {
            "Accept": "application/xml",
            "Content-Type": "application/xml",
            "Accept-Language": "en-US",
            "User-Agent": "MetarMaps/1.0",
        }

    def _get_full_url(self, path: str):
        return f"{self.BASE_URL}{path}"

    def _request(self, method, url: str, data: dict = None):
        method = method.upper()
        params = {
            "method": method,
            "url": url,
            "headers": self._get_headers(),
        }
        if method in ["POST", "PATCH"] and data:
            params["data"] = data
        response = requests.request(**params)
        response.raise_for_status()
        return response

    def get(self, path: str):
        url = self._get_full_url(path)
        return self._request("GET", url)
