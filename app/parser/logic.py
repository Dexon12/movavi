import requests

from typing import Optional

from app.parser.base import ParseByRequests
from global_config import settings


class MovaviParse(ParseByRequests):
    @property
    def payload(self):
        payload = {
            "email": self.email
        }
        return payload

    def checker(self) -> Optional[bool]:
        try:
            proxies = {
                "http": self.proxy,
                "https": self.proxy
            }
            response = requests.post(settings.URL, json=self.payload, proxies=proxies)
            if response.status_code == 500:
                print(f"[CHECKER]: Some request errorm response - {response}")
                return None
            elif response.status_code == 404:
                return False
            elif response.status_code == 200:
                return True
            elif response.status_code == 429:
                print(f"[CHECKER]: Too many requests, please change the proxy, response - {response}")
                return None
        except requests.RequestException as e:
            print(f"[CHECKER]: Error while request - {e}")
            return None
        