import os
import sys
import json
from unittest.mock import MagicMock
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Calil_API


@pytest.fixture(scope="session")
def API_client():
    with open("test/sample_apiresp.json", "r", encoding="utf-8") as f:
        api_resp = json.load(f)
    mock_response_library = MagicMock()
    mock_response_library.json = MagicMock(
        side_effect=api_resp["library_sample_resp"])
    mock_session = MagicMock()
    ret_response = [mock_response_library]
    for resp in api_resp["check_sample_resp"]:
        mock_response_check = MagicMock()
        mock_response_check.json = MagicMock(return_value=resp)
        ret_response.append(mock_response_check)
    mock_session.get = MagicMock(side_effect=ret_response)

    client = Calil_API.Client("hoge")
    client.session = mock_session
    return client
    # client.library(pref="東京都",city="千代田区")
    # print(list(client.check(isbns=[4334926940],systemids=["Special_Courts"])))
    # for d in client.check(isbns=[4334926940],systemids=["Special_Courts"]):
    #    print(d)


def test_library(API_client):
    resp = API_client.library(pref="東京都", city="千代田区")
    r = [lib["short"] for lib in resp]
    assert r == ["法務図書館", "東京本館"]


def test_check(API_client):
    ass_resp = {
        "4334926940": {
            "Tokyo_Setagaya": {
                "status": "OK",
                "reserveurl": "http://libweb.tokyo.jp/123",
                "libkey": {
                    "玉川台": "貸出可",
                    "世田谷": "貸出中",
                    "経堂": "館内のみ"
                }
            }
        },
        "4088700104": {
            "Tokyo_Setagaya": {
                "status": "Running",
                "reserveurl": "",
                "libkey": {}
            }
        }
    }
    resp = list(API_client.check(
        isbns=[4334926940, 4088700104], systemids=["Tokyo_Setagaya"]))[-1]
    assert resp == ass_resp


@pytest.mark.parametrize("arg",[{},{"city":"千代田区"}])
def test_library_raise(API_client,arg):
    with pytest.raises(ValueError):
        API_client.library(**arg)
