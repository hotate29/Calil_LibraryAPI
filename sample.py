import calil_rap.calil_API as calil_API
import json

calil_API.key = "API_KEY"

# 東京都中京区の図書館の情報
# 引数は公式の仕様書（https://calil.jp/doc/api_ref.html）
# に準ずる

# geocodeはTupleとかで
calil_API.library(geocode=(136.7163027,35.390516),limit=10)

obj = calil_API.library(pref="東京都",city="中央区")
r = obj.API_call() # listで帰ってくる
for item in r:
    # キーは公式の仕様書（https://calil.jp/doc/api_ref.html）
    # に準ずる
    print(item["formal"])
    print(item["url_pc"])

# 建設産業図書館
# http://www.ejcs.co.jp/library/cil.html
# 日本経済研究センターライブラリー
# https://www.jcer.or.jp/lib/
# 国立映画アーカイブ図書室
# https://www.nfaj.go.jp/visit/library/
# ...

obj = calil_API.check(isbn=4834000826,systemid="Aomori_Pref")
r = obj.API_call() # ジェネレーターが帰ってくる
for res in r:
    # resはdict。キーとかは公式の仕様書に準ずる（URL上記）
    # APIの都合上2秒毎にしかyieldされない
    print(json.dumps(res,indent=2))

# 複数指定もできる
obj = calil_API.check(isbn=(4834000826,4041069513),systemid=("Aomori_Pref","Shiga_Pref"))
