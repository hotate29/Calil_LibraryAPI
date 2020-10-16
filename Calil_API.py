from typing import Any, Dict, Generator, List, Tuple, Union
import os
import time

import requests


class Client:
    def __init__(self, api_key: str = None) -> None:
        """
        Parameters
        ----------
        api_key : str
            APIのキー。指定しなかった場合は環境変数"CALIL_API_KEY"から取得。
            無かったらエラー
        """
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
        """
        図書館を検索する

        Parameters
        ----------
        pref : str default None
            都道府県の名前（"北海道" とか）
        city : str default None
            市区町村の名前（"札幌市" とか）
        systemid : str default None
            図書館のシステムid（"Hokkaido_Sapporo" とか）
        geocode : (緯度,経度) default None
            この地点の近い順に図書館を出力する
        limit : int default None
            取得する図書館の件数を指定

        Returns
        -------
        res : list
            検索結果

        Raises
        ------
        ValueError
            pref systemid geocodeを指定しなかった場合。
            cityを指定したものの、prefが指定さていなかった場合。
        """
        if (pref == systemid == geocode is None):
            raise ValueError  # あとでかんがえる
        if pref is None and bool(city):
            raise ValueError  # あとでかんがえる

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
        """
        図書館の蔵書を検索する

        Parameters
        ----------
        isbns : intが入ったtupleもしくはlist
            検索する書籍のisbn
        systemids : strが入ったtupleもしくはlist
            検索する図書館のsystemid
        wait : int default 2
            ポーリングの間隔を指定する

        Returns
        -------
        res : dict
            検索結果

        Raises
        ------
        ValueError
            isbns systemidsのどれかを指定しなかった場合
            waitを2未満に指定した場合
        """
        if len(isbns) == 0 or len(systemids) == 0 or wait < 2:
            raise ValueError  # 後で考える

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
