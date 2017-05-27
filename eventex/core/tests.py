from eventex.core.views import home


def test_home(rf):
    req = rf.get('/')
    resp = home(req)
    assert 200, resp.status_code
