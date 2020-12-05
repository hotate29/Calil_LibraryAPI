import sys
sys.path.append('./')
from Calil_API import Client


API_KEY = ""
Client = Client(API_KEY)

pref = input("都道府県名:\n")
city = input("市区町村名:\n")
resp = Client.library(pref,city)

if resp == []:
    print("なし")
else:
    for lib in resp:
        print(lib.formal)
        print(f"https://calil.jp/library/{lib.libid}/{lib.formal}".replace(" ",""))
