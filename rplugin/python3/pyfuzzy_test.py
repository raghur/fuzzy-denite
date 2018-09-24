import os
from pyfuzzy import fuzzyMatches, isMatch
if os.getenv("FUZZY_CMOD"):
    from test import scoreMatchesStr
else:
    from pyfuzzy import scoreMatches


def scoreMatchesProxy(q, c, limit, key=None, ispath=True):
    if os.getenv("FUZZY_CMOD"):
        return scoreMatchesStr(q, c, limit, ispath)
    else:
        return scoreMatches(q, c, limit, key, ispath)


lines = []
with open("neomru_file") as fh:
    lines = [line.strip() for line in fh.readlines()]


def test_is_match():
    c = "D:/code/go/src/github.com/raghur/fuzzy-denite/lib/api.pb.go"
    match, positions, *rest = isMatch("api", c)
    assert match


def test_match_should_find_at_end():
    c = "D:/code/go/src/github.com/raghur/fuzzy-denite/lib/api.pb.go"
    match, positions, *rest = isMatch("api.pb.go", c)
    assert match

def test_match_should_find_at_end1():
    c = "D:/code/go/src/github.com/raghur/fuzzy-denite/lib/test_main.py"
    match, positions, *rest = isMatch("test", c)
    assert match


def test_must_find_matches_should_work_correctly_when_query_has_char_repeated():
    # in this case t-es-t - the t repeats
    # when looking right, we should not be bounded by the last found result
    # endpoint
    c = ["D:/code/go/src/github.com/raghur/fuzzy-denite/lib/test_main.py"]
    results = list(fuzzyMatches("test", c, 10))
    assert len(results) == 1

def test_must_find_matches_should_work_when_match_extends_to_the_right():
    c = ["xxxxxxx_a_g_c_g_d_e_f"]
    results = list(fuzzyMatches("gcf", c, 10))
    assert len(results) == 1

def test_must_find_matches_after_failed_partial_matches():
    lines = ["/this/a/is/pi/ap/andnomatchlater"]
    results = list(scoreMatchesProxy("api", lines, 10, ispath=True))
    assert len(results) == 1

def test_must_search_case_insensitively():
    results = list(scoreMatchesProxy("ME", lines, 10, ispath=True))
    assert results[0][0].endswith("README.md")

def test_must_score_camel_case_higher():
    c = ["/this/is/fileone.txt", "/this/is/FileOne.txt"]
    results = list(scoreMatchesProxy("fo", c, 10, ispath=True))
    assert results[0][0].endswith("FileOne.txt")


def test_must_score_camel_case_higher1():
    results = list(scoreMatchesProxy("rv", lines, 10, ispath=True))
    assert results[0][0].endswith("RelVer")

def test_must_prefer_match_at_end(benchmark):
    results = benchmark(lambda: list(scoreMatchesProxy("api", lines, 10, ispath=True)))
    assert results[0][0].endswith("api.pb.go")


def test_must_prefer_match_after_separators(benchmark):
    results = benchmark(lambda: list(scoreMatchesProxy("rct", lines, 10, ispath=True)))
    assert results[0][0].endswith("root_cmd_test.go")


def test_must_prefer_longer_match(benchmark):
    results = benchmark(lambda: list(scoreMatchesProxy("fuzz", lines, 10, ispath=True)))
    assert results[0][0].endswith("gofuzzy.py")
    assert results[1][0].endswith("pyfuzzy.py")


def test_must_score_cluster_higher(benchmark):
    results = benchmark(lambda: list(scoreMatchesProxy("cli", lines, 10, ispath=True)))
    assert results[0][0].endswith("cli.go")
    assert results[1][0].endswith("client.go")


def test_must_ignore_position_for_non_file_matching():
    c = ["/this/is/fileone.txt", "/that/was/FileOne.txt"]
    results = list(scoreMatchesProxy("is", c, 10, ispath=False))
    assert results[0][0].endswith("fileone.txt")

