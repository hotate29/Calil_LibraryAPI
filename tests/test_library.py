from calilapi import Library


def test_library():
    inp = {
        "category": "MEDIUM",
        "city": "大津市",
        "short": "北図書館",
        "libkey": "北館",
        "pref": "滋賀県",
        "primary": False,
        "faid": None,
        "geocode": "135.911394,35.112051",
        "systemid": "Shiga_Otsu",
        "address": "滋賀県大津市堅田ニ丁目1-11 北部地域文化センター内",
        "libid": "103528",
        "tel": "077-574-0145",
        "systemname": "滋賀県大津市",
        "isil": "JP-1002047",
        "post": "520-0243",
        "url_pc": "https://www.library.otsu.shiga.jp/",
        "formal": "大津市北図書館"}

    library = Library(**inp)
    out = {'category': 'MEDIUM',
           'city': '大津市',
           'short': '北図書館',
           'libkey': '北館',
           'pref': '滋賀県',
           'primary': False,
           'faid': None,
           'geocode': '135.911394,35.112051',
           'geocode_tuple': (135.911394,35.112051),
           'systemid': 'Shiga_Otsu',
           'address': '滋賀県大津市堅田ニ丁目1-11 北部地域文化センター内',
           'libid': '103528',
           'tel': '077-574-0145',
           'systemname': '滋賀県大津市',
           'isil': 'JP-1002047',
           'post': '520-0243',
           'url_pc': 'https://www.library.otsu.shiga.jp/',
           'formal': '大津市北図書館'}
    assert library.asdict() == out
