from typing import Any, Dict, Final, Generator, Iterable, List, Optional, Tuple, Union
import os
import time

import requests
from requests.sessions import Session

from .library import Library


def statuscode_check(status_code: int):
    if status_code != requests.codes.ok:
        raise Exception(
            f"The HTTP status code returned by the API was {status_code}")
    return True


class Client:
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Parameters
        ----------
        api_key : str
            APIのキー。指定しなかった場合は環境変数"CALIL_API_KEY"から取得。
            無かったらエラー
        """
        self.API_KEY: str
        if api_key is None:
            self.API_KEY = os.environ["CALIL_API_KEY"]
        else:
            self.API_KEY = api_key
        self.session: Final[Session] = requests.session()

    def library(self,
                pref: Optional[str] = None,
                city: Optional[str] = None,
                systemid: Optional[str] = None,
                geocode: Optional[Tuple[float, float]] = None,
                limit: Optional[int] = None) -> List[Library]:
        """
        図書館を検索する

        Parameters
        ----------
        pref : str default None
            都道府県の名前（"北海道"）
        city : str default None
            市区町村の名前（"札幌市"）
        systemid : str default None
            図書館のシステムid（"Hokkaido_Sapporo"）
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
        if pref is not None:
            if not isinstance(pref, str):
                raise TypeError("The pref argument must be of type str")
        if city is not None:
            if not isinstance(city, str):
                raise TypeError("The city argument must be of type str")
        if systemid is not None:
            if not isinstance(systemid, str):
                raise TypeError("The systemid argument must be of type str")
        if limit is not None:
            if not isinstance(limit, int):
                raise TypeError("The limit argument must be of type int")

        if (pref == systemid == geocode) and (pref is None):
            raise ValueError(
                "Arguments pref and one of systemid and geocode must be specified")
        if pref is None and bool(city):
            raise ValueError(
                "Along with the argument city, the argument pref must also be specified")

        EndPoint: Final[str] = "https://api.calil.jp/library"

        params: Dict[str, Union[str, int]] = {
            "appkey": self.API_KEY,
            "format": "json",
            "callback": ""
        }
        for key, value in zip(("pref", "city", "systemid", "limit"),
                              (pref, city, systemid, limit)):
            if value is not None:
                params[key] = value

        resp = self.session.get(EndPoint, params=params)
        statuscode_check(resp.status_code)
        return [Library(**lib) for lib in resp.json()]

    def check(self,
              isbns: Iterable[int],
              systemids: Iterable[str],
              wait: int = 2) -> Generator[Dict[str, Any], None, None]:
        """
        図書館の蔵書を検索する

        Parameters
        ----------
        isbns : intが入ったtupleに変換できるもの
            検索する書籍のisbn
        systemids : strが入ったtupleに変換できるもの
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

        isbns = tuple(isbns)
        systemids = tuple(systemids)
        if len(isbns) > 100 or min(
                len(isbns),
                len(systemids)) == 0 or wait < 2:
            raise ValueError  # 後で考える
        EndPoint: Final[str] = "https://api.calil.jp/check"
        params = {
            "appkey": self.API_KEY,
            "isbn": ",".join(str(isbn) for isbn in isbns),
            "systemid": ",".join(systemids),
            "format": "json",
            "callback": "no"
        }

        resp = self.session.get(EndPoint, params=params)
        statuscode_check(resp.status_code)
        resp = resp.json()
        yield resp["books"]
        while resp["continue"]:
            time.sleep(wait)
            params = {
                "appkey": self.API_KEY,
                "session": resp["session"],
                "format": "json",
                "callback": "no"
            }
            resp = self.session.get(EndPoint, params=params)
            statuscode_check(resp.status_code)
            resp = resp.json()
            yield resp["books"]
