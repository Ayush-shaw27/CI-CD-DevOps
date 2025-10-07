# tests/test_reporter.py
from reporter.reporter import Reporter

def test_summary_and_json():
    f = [{"title":"t1","description":"d","severity":"low"}]
    r = Reporter(f, repo="r")
    j = r.to_json(pretty=False)
    assert '"findings"' in j
    sd = r.summary_dict()
    assert sd["LOW"] == 1
    assert sd["TOTAL"] == 1
