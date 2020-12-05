import sys
sys.path.append('./')
from Calil_API import Client


API_KEY = ""
Client = Client.Client(API_KEY)

pref = input("都道府県名:\n")
city = input("市区町村名:\n")
r = Client.library(pref,city)

if r == []:
    print("なし")
else:
    for lib in r:
        print(lib.formal)
        print(f"https://calil.jp/library/{lib.libid}/{lib.formal}".replace(" ",""))
