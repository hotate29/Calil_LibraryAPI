from typing import Generator
import requests
import asyncio
import aiohttp

key = ""


class library():
    def __init__(
            self,
            pref=None,
            city=None,
            systemid=None,
            geocode=None,
            limit=None) -> None:
        if pref is None and systemid is None and geocode is None:
            raise TypeError(
                "There are not enough arguments.\n\
                You need to specify one of pref, systemid, geocode.")
        if city and pref is None:
            raise TypeError("Please specify the pref")
        self.pref = pref
        self.city = city
        self.systemid = systemid
        self.geocode = geocode
        self.limit = limit

    def API_call(self) -> list:
        url = self._library_URL_Generate(
            self.pref,
            self.city,
            self.systemid,
            self.geocode,
            self.limit)
        API_res = requests.get(url=url)
        if API_res.status_code != 200:
            raise Exception(f"API response code {API_res.status_code}")
        API_res.encoding = "UTF-8"
        return API_res.json()

    def _library_URL_Generate(
            self,
            pref,
            city,
            systemid,
            geocode,
            limit) -> str:
        url = f"http://api.calil.jp/library?appkey={key}&format=json&callback= "
        if pref:
            url += f"&pref={pref}"
        if city:
            url += f"&city={city}"
        if systemid:
            url += f"&systemid={systemid}"
        if geocode:
            url += f"&geocode={geocode[0]},{geocode[1]}"
        if limit:
            url += f"&limit={limit}"
        return url


class check():

    def __init__(self, isbn, systemid) -> None:
        if type(isbn) in (tuple, list):
            if len(isbn) == 0:
                raise TypeError("isbn argument must be int type")
            isbns = ",".join(map(str,isbn))
        elif isinstance(isbn, int):
            isbns = isbn
        else:
            raise TypeError("isbn type is int tuple or list")
        if type(systemid) in (tuple, list):
            if len(systemid) == 0:
                raise TypeError("systemid argument must be str type")
            ids = ",".join(systemid)
        elif isinstance(systemid, str):
            ids = systemid
        else:
            raise TypeError("systemid type is str tuple or list")
        self.isbn = isbn
        self.systemid = systemid
        self.call_URL = f"http://api.calil.jp/check?appkey={key}&isbn={isbns}&systemid={ids}&format=json&callback=no"
        print(self.call_URL)

    def API_call(self) -> Generator:
        loop = asyncio.get_event_loop()
        count = 1
        polling = None
        flag = True
        URL = self.call_URL
        while(flag):
            if count == 2:
                URL = f"http://api.calil.jp/check?appkey={key}&session={session}&format=json&callback=no"
            r = loop.run_until_complete(self._call(URL, polling=polling))
            if r["continue"] == 0:
                flag = False
            else:
                session = r["session"]
                count += 1
                polling = True
            yield r

    _c = 1

    async def _call_Test(self, URL, polling=False) -> dict:
        print(URL, polling)
        if polling:
            await asyncio.sleep(2)
        res = {"session": "session", "continue": self._c}
        self._c = 0
        return res

    async def _call(self, url: str, polling=False) -> dict:
        if polling:
            await asyncio.sleep(2)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
