from pyfuzzy import scoreMatches, fuzzyMatches
lines = []
with open("neomru_file") as fh:
    lines = [line.strip() for line in fh.readlines()]


def test_must_prefer_match_at_end():
    results = list(scoreMatches(fuzzyMatches("api", lines, 10), 10))
    assert results[0][0].endswith("api.pb.go")


def test_must_prefer_match_after_separators():
    results = list(scoreMatches(fuzzyMatches("rct", lines, 10), 10))
    assert results[0][0].endswith("root_cmd_test.go")
