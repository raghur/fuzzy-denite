from pyfuzzy import scoreMatches, fuzzyMatches, isMatch

lines = []
with open("neomru_file") as fh:
    lines = [line.strip() for line in fh.readlines()]


def test_is_match():
    c = "D:/code/go/src/github.com/raghur/fuzzy-denite/lib/api.pb.go"
    match, positions = isMatch("api", c, 0, len(c))
    assert match


def test_match_should_find_at_end():
    c = "D:/code/go/src/github.com/raghur/fuzzy-denite/lib/api.pb.go"
    match, positions = isMatch("api.pb.go", c, 0, len(c))
    assert match


def test_must_find_matches_after_failed_partial_matches():
    lines = ["/this/a/is/pi/ap/andnomatchlater"]
    results = list(scoreMatches(fuzzyMatches("api", lines, 10), 10))
    assert len(results) == 1


def test_must_prefer_match_at_end(benchmark):
    results = benchmark(lambda: list(scoreMatches(fuzzyMatches("api", lines, 10), 10)))
    assert results[0][0].endswith("api.pb.go")


def test_must_prefer_match_after_separators(benchmark):
    results = benchmark(lambda: list(scoreMatches(fuzzyMatches("rct", lines, 10), 10)))
    assert results[0][0].endswith("root_cmd_test.go")


def test_must_prefer_longer_match(benchmark):
    results = benchmark(lambda: list(scoreMatches(fuzzyMatches("fuzz", lines, 10), 10)))
    assert results[0][0].endswith("gofuzzy.py")
    assert results[1][0].endswith("pyfuzzy.py")


def test_must_score_cluster_higher(benchmark):
    results = benchmark(lambda: list(scoreMatches(fuzzyMatches("cli", lines, 10), 10)))
    assert results[0][0].endswith("cli.go")
    assert results[1][0].endswith("link.txt")
