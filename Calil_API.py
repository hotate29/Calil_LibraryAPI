from typing import Any, Dict, Generator, List, Tuple, Union
import os
import time

import requests


class Client:
    def __init__(self, api_key: str = None) -> None:
        if api_key is None:
            self.API_KEY = os.environ["CALIL_API_KEY"]
        else:
            self.API_KEY = api_key
        self.session = requests.session()

    def library(self,
                pref: str = None,
                city: str = None,
                systemid: str = None,
                geocode: Tuple[float, float] = None,
                limit: int = None) -> List[Dict[str, Any]]:
        if (pref == systemid == geocode is None):
            raise Exception  # あとでかんがえる

        params: Dict[str, Union[str, int]] = {
            "appkey": self.API_KEY,
            "format": "json",
            "callback": ""
        }
        for k, v in (("pref", pref), ("city", city),
                     ("systemid", systemid), ("limit", limit)):
            if v is not None:
                params[k] = v
        r = self.session.get("https://api.calil.jp/library", params=params)
        return r.json()

    def check(self,
              isbns: Union[List[int], Tuple[int], Tuple] = tuple(),
              systemids: Union[List[str], Tuple[str], Tuple] = tuple(),
              wait: int = 2) -> Generator[Dict[str, Any], None, None]:
        if len(isbns) == 0 or len(systemids) == 0 or wait < 2:
            raise Exception  # 後で考える

        params = {
            "appkey": self.API_KEY,
            "isbn": ",".join(str(isbn) for isbn in isbns),
            "systemid": ",".join(systemids),
            "format": "json",
            "callback": "no"
        }

        r = self.session.get("https://api.calil.jp/check", params=params)
        resp = r.json()
        yield resp["books"]
        while resp["continue"]:
            time.sleep(wait)
            params = {
                "appkey": self.API_KEY,
                "session": resp["session"],
                "format": "json",
                "callback": "no"
            }
            r = self.session.get(
                "https://api.calil.jp/check", params=params)

            resp = r.json()
            yield resp["books"]
