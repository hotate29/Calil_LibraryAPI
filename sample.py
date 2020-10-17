import Calil_API
import json

client = Calil_API.Client("API_KEY")


# 引数は公式の仕様書（https://calil.jp/doc/api_ref.html）
# に準ずる
# geocodeはTupleとかで
client.library(geocode=(136.7163027, 35.390516), limit=10)

# 東京都中京区の図書館の情報
res = client.library(pref="東京都", city="中央区")
for item in res:
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

# 引数はtupleかlistで
res = client.check(isbns=(4834000826,), systemids=("Aomori_Pref",))
for r in res:  # ジェネレーターが帰ってくる
    # dictがyieldされる。キーとかは公式の仕様書に準ずる（URL上記）
    # APIの都合上2秒毎にしかyieldされない
    print(json.dumps(r, indent=2))

# 複数指定もできる
res = client.check(
    isbns=(
        4834000826, 4041069513),
    systemids=(
        "Aomori_Pref", "Shiga_Pref"))
