calilの[図書館API](https://calil.jp/doc/api.html)のラッパー

```python
from calilapi import Client

client = Client("API_KEY")
```

### 図書館データベース
```python
resp = client.library(pref="京都府",city="京都市",systemid=None,limit=10)
```
引数は公式の仕様書とほぼ同じ。（https://calil.jp/doc/api_ref.html）  
Libraryインスタンスが入ったリストが帰ってくる
```python
print(type(resp[0]))
# <class 'Calil_API.Library.Library'>

for library in resp:
    print(lib.formal)
    print(lib.url_pc)
# 京都市こどもみらい館子育て図書館
# https://calil.jp/library/102146/京都市こどもみらい館子育て図書館
# 京都市下京図書館
# https://calil.jp/library/102147/京都市下京図書館
# 京都市中央図書館
# ...
```

### 蔵書検索
```python
resp = client.check(isbns=(4834000826,),systemids=("Aomori_Pref",))
for res in resp:
    print(res)
    # ずらずら～
```
APIから受け取った内容の["books"]を切り取って返します。
