calilの[図書館API](https://calil.jp/doc/api.html)のラッパー、かなり適当です。

```python
import calil_rap.calil_API as calil_API

client = Calil_API.Client("API_KEY")
```

### 図書館データベース
```python
r = calil_API.library(pref="京都府",city="京都市",systemid=None,limit=10)
```
引数は公式の仕様書とほぼ同じ。（https://calil.jp/doc/api_ref.html）
```python
print(r)
# ずらずら～
```
APIから受け取ったのをそのまま返してます。

### 蔵書検索
```python
r = calil_API.check(isbn=4834000826,systemid="Aomori_Pref")
for res in r:
    print(res)
    # ずらずら～
```
