import httpx

def test_delay_route():
    r = httpx.get("http://localhost:8000/h2test/delay?ms=200")
    assert r.status_code == 200
    assert r.json()["delayed"] == "200ms"

def test_echo_route():
    r = httpx.get("http://localhost:8000/h2test/echo", headers={"X-Test": "Hello"})
    assert r.status_code == 200
    assert r.json()["headers"]["x-test"] == "Hello"

def test_error_route():
    r = httpx.get("http://localhost:8000/h2test/error?code=503")
    assert r.status_code == 503
