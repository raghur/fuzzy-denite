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
scoreMatches = test.scoreMatchesStr
lines = []
with open("neomru_file") as fh:
    lines = [line.strip() for line in fh.readlines()]

# for i in range(1000):
# results = scoreMatches("api", lines, 10)
# assert results[0][0].endswith("api.pb.go")

# print("data :", lines[:10])
results = scoreMatches("rct", lines, 10)
print("results: ", results)
assert results[0][0].endswith("root_cmd_test.go")


# results = scoreMatches("fuzz", lines, 10)
# assert results[0][0].endswith("gofuzzy.py")
# assert results[1][0].endswith("pyfuzzy.py")


# results = scoreMatches("cli", lines, 10)
# assert results[0][0].endswith("cli.go")
# assert results[1][0].endswith("client.go")

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
