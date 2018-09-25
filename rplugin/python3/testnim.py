import test
import copy
import sys


# c = {'abbr':
#  '~/code/go/src/github.com/raghur/fuzzy-denite/rplugin/python3/denite/filter/matcher/fuzzymatcher.py',
#  'source_name': 'file_mru',
#  'word':
#  '~/code/go/src/github.com/raghur/fuzzy-denite/rplugin/python3/denite/filter/matcher/fuzzymatcher.py',
#  'source_index': 0,
#  'action__path': '/home/raghu/code/go/src/github.com/raghur/fuzzy-denite/rplugin/python3/denite/filter/matcher/fuzzymatcher.py'}

# print(test.scoreMatches("github", [c], 1))
def printResults(query, results):
    print()
    print("query: %s, results: " % query, results)

def scoreMatches(q, c, limit, ispath):
    idxArr = test.scoreMatchesStr(q, c, limit, ispath)
    results = []
    for i in idxArr:
        results.append((c[i[0]],i[1]))
    return results

lines = []
with open("neomru_file") as fh:
    lines = [line.strip() for line in fh.readlines()]

results = scoreMatches("api", lines, 10, True)
printResults("api", results)
assert results[0][0].endswith("api.pb.go")

results = scoreMatches("rct", lines, 10, True)
printResults("rct", results)
assert results[0][0].endswith("root_cmd_test.go")

results = scoreMatches("fuzz", lines, 10, True)
printResults("fuzz", results)
assert results[0][0].endswith("pyfuzzy.py")
assert results[1][0].endswith("gofuzzy.py")

results = scoreMatches("cli", lines, 10, True)
printResults("cli", results)
assert results[0][0].endswith("listblogs.go")
assert results[1][0].endswith("cli.go")

results = scoreMatches("testn", lines, 10, True)
printResults("testn", results)
assert results[0][0].endswith("test_main.py")


# c = ["fileone.txt/is/this/", "/this/is/fileone.txt", "/this/is/FileOne.txt"]
# r = []
# for x in test.scoreMatchesStr("fo", c, 10):
#     r.append(x)
# # print(results)
# assert r[0][0].endswith("FileOne.txt")
# if i % 100  == 0:
#     sys.stdout.write(".")
#     sys.stdout.flush()
# c = ["fileone.txt/is/this/", "/this/is/fileone.txt", "/this/is/FileOne.txt"]
# results = list(test.scoreMatchesStr("fo", c, 10))
# print(results)
