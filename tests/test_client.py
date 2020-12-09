from unittest import mock

import pytest

from calilapi import Client


def mocked_requests_session(status_code,json_data):
    class MockResponse:
        def __init__(self,status_code,json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data
    # mock_renponse = MockResponse(status_code,json_data)
    mock_Session = mock.MagicMock(name="mocksession")
    mock_Session.get = mock.MagicMock(return_value=MockResponse(status_code,json_data))
    mock_session = mock.MagicMock(return_value=mock_Session)

    return mock_session


@pytest.mark.parametrize("status_code,json_data",[
    (100,[{}]),
    (500,[{}])
])
def test_library_ng_status_code(status_code,json_data):
    mock_session = mocked_requests_session(status_code,json_data)
    with mock.patch("requests.session",mock_session):
        client = Client("")
        with pytest.raises(Exception):
            client.library("テスト","テスト")


@pytest.mark.parametrize("status_code,json_data",[
    (100,[{}]),
    (500,[{}])
])
def test_check_ng_status_code(status_code,json_data):
    mock_session = mocked_requests_session(status_code,json_data)
    with mock.patch("requests.session",mock_session):
        client = Client("")
        r = client.check(["a"],["a"])
        with pytest.raises(Exception):
            next(r)


def test_ok_status_code():
    json_data = {}
    json_data["city"] = "1.0,1.0"
    json_data["category"] = "1.0,1.0"
    json_data["short"] = "1.0,1.0"
    json_data["libkey"] = "1.0,1.0"
    json_data["pref"] = "1.0,1.0"
    json_data["primary"] = False
    json_data["faid"] = None
    json_data["systemid"] = "1.0,1.0"
    json_data["address"] = "1.0,1.0"
    json_data["libid"] = "1.0,1.0"
    json_data["tel"] = "1.0,1.0"
    json_data["systemname"] = "1.0,1.0"
    json_data["isil"] = "1.0,1.0"
    json_data["post"] = "1.0,1.0"
    json_data["url_pc"] = "1.0,1.0"
    json_data["formal"] = "1.0,1.0"
    json_data["geocode"] = "1.0,1.0"

    mock_session = mocked_requests_session(200,[json_data])
    with mock.patch("requests.session",mock_session):
        client = Client("")
        r = client.library("テスト","テスト")
        print(r)


@pytest.mark.parametrize("pref,city,geocode,systemid,limit",[
    (0,None,None,None,None),
    (None,0,None,None,None),
    (None,None,0,None,None),
    (None,None,(1,1.0),None,None),
    (None,None,None,0,None),
    (None,None,None,None,"")
])
def test_library_arg_ng_type(pref,city,geocode,systemid,limit):
    client = Client("")
    with pytest.raises(TypeError):
        client.library(pref,city,systemid,geocode,limit)


@pytest.mark.parametrize("pref,city,geocode,systemid,limit",[
    (None,None,None,None,None),
    (None,"",None,"",None),
])
def test_library_arg_unspecified(pref,city,geocode,systemid,limit):
    client = Client("")
    with pytest.raises(ValueError):
        client.library(pref,city,systemid,geocode,limit)


def test_client_token_env(monkeypatch):
    monkeypatch.setenv("CALIL_API_KEY","hoge")
    Client()
